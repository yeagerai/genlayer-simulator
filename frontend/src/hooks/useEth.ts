import { recoverTransactionAddress, toHex, toRlp } from 'viem';
import type { TransactionSerializedLegacy } from 'viem';
import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts';
import type { Address } from '@/types';

// Abstract 1+ level to automatically sign with current wallet? what about unit test?
export function useEth() {
  const getAccountFromPrivatekey = (privateKey: Address) => {
    return privateKeyToAccount(privateKey);
  };

  const getPrivateKey = () => {
    return generatePrivateKey();
  };

  // Better typing here?
  const encodeTransactionData = (params: any[]) => {
    return toRlp(params.map((param) => toHex(param)));
  };

  async function signTransaction(
    privateKey: Address,
    data: Array<unknown>,
    to?: Address,
  ): Promise<TransactionSerializedLegacy> {
    const account = getAccountFromPrivatekey(privateKey);
    const encodedData = encodeTransactionData(data);
    return account.signTransaction({ data: encodedData, to, type: 'legacy' });
  }

  return {
    getAccountFromPrivatekey,
    getPrivateKey,
    signTransaction,
    recoverTransactionAddress,
  };
}
