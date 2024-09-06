import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useWallet } from '@/hooks/useWallet';
import { recoverTransactionAddress } from 'viem';

const testPrivateKey =
  '0x90efb1e7b1cedc8b4c9c6be652b93a1549e4cfa94d43f5918e60a9cd5f8cf479'; // ! NEVER USE THIS PRIVATE KEY
const testAddress = '0x779769CEFAEEBF0f388F9Bc7072B08139084B8b0';
const testData = [
  '0x70997970c51812dc3a010c7d01b50e0d17dc79c8',
  1000000000000000000n,
];
const testSignedTransaction =
  '0xf87e8080808080b5f4aa307837303939373937306335313831326463336130313063376430316235306530643137646337396338880de0b6b3a76400001ca09047ca41a2f96e45360ec4e84bd83e805cd3de564f235472e540acfe8fdb794ea077597cc9e359e6bf0889b476657f2f892f774d0d776a5a58776fb15975a97a26';

describe('useWallet', () => {
  const wallet = useWallet();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should generate a private key of the right length', () => {
    const result = wallet.generatePrivateKey();
    expect(result).toHaveLength(testPrivateKey.length);
  });

  it('should convert a private key to an account', () => {
    const result = wallet.privateKeyToAccount(testPrivateKey);
    expect(result.address).toBe(testAddress);
  });

  it('it should sign a transaction and verify the signature and deduce the address', async () => {
    const signedTransaction = await wallet.signTransaction({
      privateKey: testPrivateKey,
      data: testData,
    });
    expect(signedTransaction).toBe(testSignedTransaction);

    const account = wallet.privateKeyToAccount(testPrivateKey);
    const txAddress = await recoverTransactionAddress({
      serializedTransaction: signedTransaction,
    });
    expect(txAddress).to.deep.equal(account.address);
  });

  it('should shorten an Ethereum address correctly', () => {
    const address = '0x1234567890abcdef1234567890abcdef12345678';
    const result = wallet.shortenAddress(address);
    expect(result).toBe('0x12...5678');
  });

  it('should shorten a non-Ethereum address correctly', () => {
    const address = 'abcdef1234567890abcdef1234567890abcdef12';
    const result = wallet.shortenAddress(address);
    expect(result).toBe('abcd...ef12');
  });

  it('should return empty string for undefined input', () => {
    const result = wallet.shortenAddress(undefined);
    expect(result).toBe('');
  });

  it('should return empty string for empty string input', () => {
    const result = wallet.shortenAddress('');
    expect(result).toBe('');
  });

  it('should handle short addresses with prefix correctly', () => {
    const address = '0x1234';
    const result = wallet.shortenAddress(address);
    expect(result).toBe('0x...34');
  });
});
