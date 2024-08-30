import { describe, it, expect, beforeEach, vi, type Mock } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useAccountsStore } from '@/stores';
import { useWallet } from '@/hooks';

const testKey1 =
  '0x4104e41989791c1e1f3a889710d8c5509b98ee62e5fabced8a3f538f5afd392b'; // ! NEVER USE THIS PRIVATE KEY
const testAddress1 = '0x858744E989D688C5f02ec2388342cc34Edf88a97';
const testKey2 =
  '0x90efb1e7b1cedc8b4c9c6be652b93a1549e4cfa94d43f5918e60a9cd5f8cf479'; // ! NEVER USE THIS PRIVATE KEY

vi.mock('@/hooks', () => ({
  useWallet: vi.fn(),
  useShortAddress: vi.fn(),
}));

describe('useAccountsStore', () => {
  let accountsStore: ReturnType<typeof useAccountsStore>;
  const mockWallet = {
    privateKeyToAccount: vi.fn(),
    generatePrivateKey: vi.fn(),
    shortenAddress: vi.fn(),
  };

  beforeEach(() => {
    setActivePinia(createPinia());
    (useWallet as Mock).mockReturnValue(mockWallet);

    // Mock localStorage
    vi.stubGlobal('localStorage', {
      getItem: vi.fn(),
      setItem: vi.fn(),
      removeItem: vi.fn(),
    });

    accountsStore = useAccountsStore();

    mockWallet.privateKeyToAccount.mockClear();
    mockWallet.generatePrivateKey.mockClear();
    mockWallet.shortenAddress.mockClear();
    (localStorage.getItem as Mock).mockClear();
    (localStorage.getItem as Mock).mockClear();
    (localStorage.removeItem as Mock).mockClear();
  });

  it('should generate a new account', () => {
    const newPrivateKey = '0xnewkey';
    mockWallet.generatePrivateKey.mockReturnValue(newPrivateKey);
    const generatedKey = accountsStore.generateNewAccount();

    expect(generatedKey).toBe(newPrivateKey);
    expect(accountsStore.privateKeys).toContain(newPrivateKey);
    expect(accountsStore.currentPrivateKey).toBe(newPrivateKey);
  });

  it('should remove an account and default to existing one', () => {
    accountsStore.privateKeys = [testKey1, testKey2];
    accountsStore.currentPrivateKey = testKey1;

    accountsStore.removeAccount(testKey1);

    expect(accountsStore.privateKeys).toEqual([testKey2]);
    expect(accountsStore.currentPrivateKey).toBe(testKey2);
  });

  it('should throw error when removing the last account', () => {
    accountsStore.privateKeys = [testKey1];

    expect(() => accountsStore.removeAccount(testKey1)).toThrow(
      'You need at least 1 account',
    );
  });

  it('should handle errors in displayAddress computation', () => {
    accountsStore.currentPrivateKey = '0xinvalidkey';

    mockWallet.privateKeyToAccount.mockImplementation(() => {
      throw new Error('Invalid private key');
    });

    const consoleSpy = vi.spyOn(console, 'error');
    consoleSpy.mockImplementation(() => {});

    expect(accountsStore.displayAddress).toBe('0x');

    consoleSpy.mockRestore();
  });

  it('should set current account', () => {
    const newPrivateKey = testKey2;
    accountsStore.setCurrentAccount(newPrivateKey);

    expect(accountsStore.currentPrivateKey).toBe(newPrivateKey);
  });

  it('should compute currentUserAddress correctly', () => {
    const privateKey = testKey1;
    const account = { address: testAddress1 };
    accountsStore.currentPrivateKey = privateKey;
    mockWallet.privateKeyToAccount.mockReturnValue(account);

    expect(accountsStore.currentUserAddress).toBe(testAddress1);
    expect(mockWallet.privateKeyToAccount).toHaveBeenCalledWith(privateKey);
  });

  it('should return an empty string for currentUserAddress when no private key is set', () => {
    accountsStore.currentPrivateKey = null;
    expect(accountsStore.currentUserAddress).toBe('');
  });
});
