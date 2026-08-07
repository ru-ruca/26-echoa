import { createReadStream } from 'node:fs';
import { createInterface } from 'node:readline';

/** JSONL 파일을 한 줄씩 파싱해 흘려보낸다 (전체를 메모리에 올리지 않는다). */
export async function* readJsonl<T>(path: string): AsyncGenerator<T> {
  const rl = createInterface({
    input: createReadStream(path, 'utf8'),
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    const trimmed = line.trim();
    if (trimmed.length === 0) continue;
    yield JSON.parse(trimmed) as T;
  }
}

/** JSONL 전체를 배열로 읽는다 (수백~수천 행 규모라 문제 없다). */
export async function readJsonlAll<T>(path: string): Promise<T[]> {
  const rows: T[] = [];
  for await (const row of readJsonl<T>(path)) rows.push(row);
  return rows;
}

/** 큰 INSERT 를 나눠 넣기 위한 청크 분할. */
export function chunk<T>(items: readonly T[], size: number): T[][] {
  const out: T[][] = [];
  for (let i = 0; i < items.length; i += size) {
    out.push(items.slice(i, i + size));
  }
  return out;
}
