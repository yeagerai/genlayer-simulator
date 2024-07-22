import { getAccountFromPrivatekey } from './accounts'
import {
  createWalletClient,
  http,
  recoverTransactionAddress,
  serializeTransaction as _serializeTransaction,
  type TransactionSerializedLegacy
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

export async function getSignedTransactionAddress(
  signedTransaction:
    | `0x02${string}`
    | `0x01${string}`
    | `0x03${string}`
    | TransactionSerializedLegacy
) {
  return await recoverTransactionAddress({
    serializedTransaction: signedTransaction
  })
}


export async function serializeTransaction (data: any) {
  return _serializeTransaction({
    ...data,
    gas: '0x', //TODO: we need to fix this later
    type: 'legacy'
  })
}