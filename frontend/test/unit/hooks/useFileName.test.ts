import { describe, it, expect } from 'vitest';
import { useFileName } from '@/hooks';

describe('useFileName composable', () => {
  const { cleanupFileName } = useFileName();

  it('should return the original name with ".gpy" when there is no period in the name', () => {
    const result = cleanupFileName('example');
    expect(result).toBe('example.gpy');
  });

  it('should replace the extension with ".gpy" if there is a period in the name', () => {
    const result = cleanupFileName('document.txt');
    expect(result).toBe('document.gpy');
  });

  it('should return ".gpy" if the name is just a period', () => {
    const result = cleanupFileName('.');
    expect(result).toBe('.gpy');
  });

  it('should handle names with multiple periods correctly', () => {
    const result = cleanupFileName('archive.tar.gz');
    expect(result).toBe('archive.gpy');
  });

  it('should return ".gpy" for an empty string', () => {
    const result = cleanupFileName('');
    expect(result).toBe('.gpy');
  });
});
