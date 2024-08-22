import { useEth } from '../../../src/hooks/useEth';
import { describe, expect, it, vi, afterEach, beforeEach } from 'vitest';

describe('SignTransaction', () => {
  const eth = useEth();

  beforeEach(() => {
    //
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('signTransaction', () => {
    const privateKey = eth.getPrivateKey();

    const data = [
      '0x70997970c51812dc3a010c7d01b50e0d17dc79c8',
      1000000000000000000n,
    ];

    it('it should sign a transaction and verify', async () => {
      const signedTransaction = await eth.signTransaction(privateKey, data);
      const account = eth.getAccountFromPrivatekey(privateKey);
      const txAddress = await eth.recoverTransactionAddress({
        serializedTransaction: signedTransaction,
      });
      expect(txAddress).to.deep.equal(account.address);
    });
  });
});
