import { getAccountFromPrivatekey } from './accounts'
import {
  createWalletClient,
  http,
  serializeTransaction as _serializeTransaction
} from 'viem'
import { mainnet } from 'viem/chains'

export const walletClient = createWalletClient({
  chain: mainnet,
  transport: http()
})

export async function signTransaction(privateKey: `0x${string}`, data: any) {
  const account = getAccountFromPrivatekey(privateKey)
  return account.signTransaction({ ...data, type: 'legacy' })
}

export async function serializeTransaction (data: any) {
  return _serializeTransaction({
    ...data,
    gas: '0x', //TODO: we need to fix this later
    type: 'legacy'
  })
}