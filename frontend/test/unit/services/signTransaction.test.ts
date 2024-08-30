import { useWallet } from '../../../src/hooks/useWallet';
import { describe, expect, it, vi, afterEach, beforeEach } from 'vitest';

describe('SignTransaction', () => {
  const { web3 } = useWallet();

  beforeEach(() => {
    //
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('signTransaction', () => {
    const privateKey = wallet.generatePrivateKey();

    const data = [
      '0x70997970c51812dc3a010c7d01b50e0d17dc79c8',
      1000000000000000000n,
    ];

    it('it should sign a transaction and verify', async () => {
      const signedTransaction = await web3.signTransaction(privateKey, data);
      const account = web3.privateKeyToAccount(privateKey);
      const txAddress = await web3.recoverTransactionAddress({
        serializedTransaction: signedTransaction,
      });
      expect(txAddress).to.deep.equal(account.address);
    });
  });
});
