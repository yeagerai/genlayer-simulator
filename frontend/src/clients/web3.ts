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

// TODO: remove ?

export type TransactionDataElement =
  | string
  | number
  | bigint
  | boolean
  | Uint8Array;

export class Web3Client {
  privateKeyToAccount(privateKey: Address) {
    return _privateKeyToAccount(privateKey);
  }

  generatePrivateKey() {
    return _generatePrivateKey();
  }

  encodeTransactionData(params: TransactionDataElement[]) {
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
    nonce,
  }: {
    privateKey: Address;
    data: TransactionDataElement[];
    to?: Address;
    value?: bigint;
    nonce: number;
  }): Promise<TransactionSerializedLegacy> {
    const account = this.privateKeyToAccount(privateKey);
    const encodedData = this.encodeTransactionData(data);
    return account.signTransaction({
      data: encodedData,
      to,
      value,
      nonce,
      type: 'legacy',
    });
  }
}
