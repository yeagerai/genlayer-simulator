import { describe, it, expect, afterEach, vi } from 'vitest';
import { useConfig } from '@/hooks';

describe('useConfig', () => {
  const original = window.location;

  afterEach(() => {
    Object.defineProperty(window, 'location', {
      value: original,
      writable: true,
    });
  });

  it('should return true for canUpdateValidators when URL includes localhost', () => {
    Object.defineProperty(window, 'location', {
      value: {
        href: 'http://localhost:8080',
        hostname: 'localhost',
      },
      writable: true,
    });

    const { canUpdateValidators } = useConfig();
    expect(canUpdateValidators.value).toBe(true);
    Object.defineProperty(window, 'location', original);
  });

  it('should return false for canUpdateValidators when URL does not include localhost', () => {
    Object.defineProperty(window, 'location', {
      value: {
        href: 'https://studio.genlayer.com',
        hostname: 'genlayer',
      },
      writable: true,
    });

    const { canUpdateValidators } = useConfig();
    expect(canUpdateValidators.value).toBe(false);
    Object.defineProperty(window, 'location', original);
  });
});
