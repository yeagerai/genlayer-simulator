import { toHex, toRlp } from 'viem';
import {
  generatePrivateKey as _generatePrivateKey,
  privateKeyToAccount as _privateKeyToAccount,
} from 'viem/accounts';
import type { TransactionSerializedLegacy } from 'viem';
import type { Address } from '@/types';

export function useWallet() {
  const privateKeyToAccount = (privateKey: Address) => {
    return _privateKeyToAccount(privateKey);
  };

  const generatePrivateKey = () => {
    return _generatePrivateKey();
  };

  const encodeTransactionData = (params: any[]) => {
    return toRlp(params.map((param) => toHex(param)));
  };

  async function signTransaction(
    privateKey: Address,
    data: Array<unknown>,
    to?: Address,
  ): Promise<TransactionSerializedLegacy> {
    const account = privateKeyToAccount(privateKey);
    const encodedData = encodeTransactionData(data);
    return account.signTransaction({ data: encodedData, to, type: 'legacy' });
  }

  return {
    privateKeyToAccount,
    generatePrivateKey,
    signTransaction,
  };
}
