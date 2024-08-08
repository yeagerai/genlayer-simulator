import { getAccountFromPrivatekey } from './accounts';

export async function signTransaction(
  privateKey: `0x${string}`,
  data: `0x${string}`,
): Promise<string> {
  const account = getAccountFromPrivatekey(privateKey);
  return account.signTransaction({ data, type: 'legacy' });
}
