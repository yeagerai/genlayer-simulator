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
    const input = {
      contractAddress: '0x58FaA28cbAA1b52F8Ec8D3c6FFCE6f1AaF8bEEB1',
      method: 'get_have_coin',
      params: []
    }

    const data = {
      method: 'get_contract_state',
      params: [input.contractAddress, input.method, []]
    }

    it('it should sign a transaction and verify', async () => {
      const signedTransaction = await signTransaction(privateKey, data)
      const account = getAccountFromPrivatekey(privateKey)
      const txAddress = await getSignedTransactionAddress(signedTransaction)
      expect(txAddress).to.deep.equal(account.address)
    })
  })
})
