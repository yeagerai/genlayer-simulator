import { describe, it, expect, beforeEach, vi } from 'vitest';
import { useConfig } from '@/hooks';

describe('useConfig', () => {
  beforeEach(() => {
    vi.stubEnv('VITE_IS_HOSTED', 'false');
  });

  it('should return true for canUpdateValidators when not in hosted environment', () => {
    vi.stubEnv('VITE_IS_HOSTED', 'false');

    const { canUpdateValidators } = useConfig();
    expect(canUpdateValidators).toBe(true);
  });

  it('should return false for canUpdateValidators when in hosted environment', () => {
    vi.stubEnv('VITE_IS_HOSTED', 'true');

    const { canUpdateValidators } = useConfig();
    expect(canUpdateValidators).toBe(false);
  });
});
