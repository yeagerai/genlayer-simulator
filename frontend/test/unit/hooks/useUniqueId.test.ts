import { describe, it, expect, vi } from 'vitest';
import { useUniqueId } from '@/hooks';
import { v4 as uuidv4 } from 'uuid';

vi.mock('uuid', () => ({
  v4: vi.fn(() => 'mocked-uuid'),
}));

describe('useUniqueId function', () => {
  it('should generate a unique ID without prefix', () => {
    const result = useUniqueId();

    expect(uuidv4).toHaveBeenCalled(); // Ensure that uuidv4 is called
    expect(result).toBe('mocked-uuid'); // Check that the result is only the UUID without prefix
  });

  it('should generate a unique ID with the correct prefix', () => {
    const prefix = 'testPrefix';
    const result = useUniqueId(prefix);

    expect(uuidv4).toHaveBeenCalled(); // Ensure that uuidv4 is called
    expect(result).toBe(`${prefix}-mocked-uuid`); // Check the format of the returned ID
  });
});
