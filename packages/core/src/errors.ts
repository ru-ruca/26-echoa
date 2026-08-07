import { ERROR_MSG } from './error-messages';

export type ErrorCode = 'NETWORK' | 'TIMEOUT' | 'SERVER' | 'NOT_FOUND' | 'VALIDATION' | 'UNKNOWN';

export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: ErrorCode,
    public readonly status?: number,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export function isAppError(error: unknown): error is AppError {
  return error instanceof AppError;
}

export type ErrorSeverity = 'error' | 'warning';

export interface ErrorClassification {
  code: ErrorCode;
  message: string;
  severity: ErrorSeverity;
  /** true면 toast/UI 표시를 건너뜀 (컴포넌트가 자체 처리) */
  skip: boolean;
}

/**
 * 에러를 분류하여 code, message, severity, skip 여부를 반환.
 * - VALIDATION → warning (입력 오류)
 * - NOT_FOUND → skip (컴포넌트가 빈 상태 UI 표시)
 * - 나머지 → error
 */
export function classifyError(error: unknown): ErrorClassification {
  if (error instanceof AppError) {
    return {
      code: error.code,
      message: error.message,
      severity: error.code === 'VALIDATION' ? 'warning' : 'error',
      skip: error.code === 'NOT_FOUND',
    };
  }

  if (error instanceof TypeError && error.message.includes('fetch')) {
    return {
      code: 'NETWORK',
      message: ERROR_MSG.NETWORK,
      severity: 'error',
      skip: false,
    };
  }

  const message = error instanceof Error ? error.message : ERROR_MSG.SERVER;
  return { code: 'UNKNOWN', message, severity: 'error', skip: false };
}
