import { recoverTransactionAddress, toHex, toRlp } from 'viem';
import {
  generatePrivateKey as _generatePrivateKey,
  privateKeyToAccount as _privateKeyToAccount,
} from 'viem/accounts';
import type {
  TransactionSerializedLegacy,
  RecoverTransactionAddressParameters,
} from 'viem';
import type { Address } from '@/types';

export class Web3Client {
  privateKeyToAccount(privateKey: Address) {
    return _privateKeyToAccount(privateKey);
  }

  generatePrivateKey() {
    return _generatePrivateKey();
  }

  encodeTransactionData(params: any[]) {
    return toRlp(params.map((param) => toHex(param)));
  }

  recoverTransactionAddress(transaction: RecoverTransactionAddressParameters) {
    return recoverTransactionAddress(transaction);
  }

  async signTransaction({
    privateKey,
    data,
    to = undefined,
    value = 0n,
  }: {
    privateKey: Address;
    data: Array<unknown>;
    to?: Address;
    value?: bigint;
  }): Promise<TransactionSerializedLegacy> {
    const account = this.privateKeyToAccount(privateKey);
    const encodedData = this.encodeTransactionData(data);
    return account.signTransaction({
      data: encodedData,
      to,
      value,
      type: 'legacy',
    });
  }
}
