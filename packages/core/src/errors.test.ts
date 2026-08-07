import { describe, it, expect } from 'vitest';
import { AppError, isAppError, classifyError } from './errors';
import { ERROR_MSG } from './error-messages';

describe('AppError', () => {
  it('message, code, status를 올바르게 저장', () => {
    const error = new AppError('not found', 'NOT_FOUND', 404);

    expect(error.message).toBe('not found');
    expect(error.code).toBe('NOT_FOUND');
    expect(error.status).toBe(404);
    expect(error.name).toBe('AppError');
  });

  it('status 없이 생성 가능', () => {
    const error = new AppError(ERROR_MSG.NETWORK, 'NETWORK');

    expect(error.status).toBeUndefined();
    expect(error.code).toBe('NETWORK');
  });

  it('Error를 상속', () => {
    const error = new AppError('test', 'UNKNOWN');

    expect(error).toBeInstanceOf(Error);
    expect(error).toBeInstanceOf(AppError);
  });
});

describe('isAppError', () => {
  it('AppError 인스턴스 → true', () => {
    expect(isAppError(new AppError('test', 'SERVER', 500))).toBe(true);
  });

  it('일반 Error → false', () => {
    expect(isAppError(new Error('test'))).toBe(false);
  });

  it('null/undefined → false', () => {
    expect(isAppError(null)).toBe(false);
    expect(isAppError(undefined)).toBe(false);
  });

  it('문자열 → false', () => {
    expect(isAppError('error')).toBe(false);
  });
});

describe('ERROR_MSG', () => {
  it('모든 메시지가 한국어', () => {
    const values = Object.values(ERROR_MSG);

    expect(values.length).toBeGreaterThan(0);
    for (const msg of values) {
      expect(msg).toMatch(/[가-힣]/);
    }
  });

  it('필수 키가 모두 존재', () => {
    expect(ERROR_MSG.NETWORK).toBeDefined();
    expect(ERROR_MSG.TIMEOUT).toBeDefined();
    expect(ERROR_MSG.SERVER).toBeDefined();
    expect(ERROR_MSG.LOAD_FAILED).toBeDefined();
    expect(ERROR_MSG.SAVE_FAILED).toBeDefined();
    expect(ERROR_MSG.FAVORITE_TOGGLE).toBeDefined();
    expect(ERROR_MSG.PROGRESS_SAVE).toBeDefined();
    expect(ERROR_MSG.REVIEW_LOAD).toBeDefined();
    expect(ERROR_MSG.REVIEW_SAVE).toBeDefined();
  });
});

describe('classifyError', () => {
  it('AppError(VALIDATION) → severity: warning', () => {
    const result = classifyError(new AppError('bad input', 'VALIDATION', 400));
    expect(result.code).toBe('VALIDATION');
    expect(result.severity).toBe('warning');
    expect(result.skip).toBe(false);
    expect(result.message).toBe('bad input');
  });

  it('AppError(NOT_FOUND) → skip: true', () => {
    const result = classifyError(new AppError('not found', 'NOT_FOUND', 404));
    expect(result.code).toBe('NOT_FOUND');
    expect(result.skip).toBe(true);
  });

  it('AppError(SERVER) → severity: error, skip: false', () => {
    const result = classifyError(new AppError('db error', 'SERVER', 500));
    expect(result.code).toBe('SERVER');
    expect(result.severity).toBe('error');
    expect(result.skip).toBe(false);
  });

  it('AppError(NETWORK) → severity: error', () => {
    const result = classifyError(new AppError(ERROR_MSG.NETWORK, 'NETWORK'));
    expect(result.code).toBe('NETWORK');
    expect(result.severity).toBe('error');
  });

  it('AppError(TIMEOUT) → severity: error', () => {
    const result = classifyError(new AppError(ERROR_MSG.TIMEOUT, 'TIMEOUT'));
    expect(result.code).toBe('TIMEOUT');
    expect(result.severity).toBe('error');
  });

  it('TypeError(Failed to fetch) → NETWORK', () => {
    const result = classifyError(new TypeError('Failed to fetch'));
    expect(result.code).toBe('NETWORK');
    expect(result.message).toBe(ERROR_MSG.NETWORK);
  });

  it('일반 Error → UNKNOWN, severity: error', () => {
    const result = classifyError(new Error('something broke'));
    expect(result.code).toBe('UNKNOWN');
    expect(result.severity).toBe('error');
    expect(result.message).toBe('something broke');
  });

  it('non-Error (문자열) → UNKNOWN, 기본 메시지', () => {
    const result = classifyError('string error');
    expect(result.code).toBe('UNKNOWN');
    expect(result.message).toBe(ERROR_MSG.SERVER);
  });
});
