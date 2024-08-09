import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts';
import type { Address } from '@/types';

export const getAccountFromPrivatekey = (privateKey: Address) => {
  return privateKeyToAccount(privateKey);
};

export const getPrivateKey = () => {
  return generatePrivateKey();
};
