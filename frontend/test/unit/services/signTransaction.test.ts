import {
  signTransaction,
  getPrivateKey,
  getAccountFromPrivatekey,
  getSignedTransactionAddress
} from '../../../src/utils'
import { describe, expect, it, vi, afterEach, beforeEach } from 'vitest'

describe('JsonRprService', () => {
  beforeEach(() => {
    //
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('signTransaction', () => {
    const privateKey = getPrivateKey()

    const data = {
        to: '0x70997970c51812dc3a010c7d01b50e0d17dc79c8',
        value: 1000000000000000000n
    }

    it('it should sign a transaction and verify', async () => {
      const signedTransaction = await signTransaction(privateKey, data)
      const account = getAccountFromPrivatekey(privateKey)
      const txAddress = await getSignedTransactionAddress(signedTransaction)
      expect(txAddress).to.deep.equal(account.address)
    })
  })
})
