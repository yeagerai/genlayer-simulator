import { describe, it, expect } from 'vitest';
import { useShortAddress } from '@/hooks/useShortAddress';

describe('useShortAddress', () => {
  const { shortenAddress } = useShortAddress();

  it('should shorten an Ethereum address correctly', () => {
    const address = '0x1234567890abcdef1234567890abcdef12345678';
    const result = shortenAddress(address);
    expect(result).toBe('0x12...5678');
  });

  it('should shorten a non-Ethereum address correctly', () => {
    const address = 'abcdef1234567890abcdef1234567890abcdef12';
    const result = shortenAddress(address);
    expect(result).toBe('abcd...ef12');
  });

  it('should return empty string for undefined input', () => {
    const result = shortenAddress(undefined);
    expect(result).toBe('');
  });

  it('should return empty string for empty string input', () => {
    const result = shortenAddress('');
    expect(result).toBe('');
  });

  it('should handle short addresses with prefix correctly', () => {
    const address = '0x1234';
    const result = shortenAddress(address);
    expect(result).toBe('0x...34');
  });
});
