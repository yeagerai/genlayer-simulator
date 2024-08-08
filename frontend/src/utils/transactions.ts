import { getAccountFromPrivatekey } from './accounts';

import type {Address} from '@/types';

export async function signTransaction(
  privateKey: Address,
  data: Address,
  to?: Address,
): Promise<string> {
  const account = getAccountFromPrivatekey(privateKey);
  return account.signTransaction({ data, to, type: 'legacy' });
}
