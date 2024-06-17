import { defineStore } from 'pinia'
import { inject, ref } from 'vue'
import type { IJsonRpcService } from '@/services'

export const useAccountsStore = defineStore('accountsStore', () => {
  const $jsonRpc = inject<IJsonRpcService>('$jsonRpc')
  const currentUserAddress = ref<string>(localStorage.getItem('mainStore.currentUserAddress') || '')

  const accounts = ref<string[]>(
    localStorage.getItem('accountsStore.accounts')
      ? (localStorage.getItem('accountsStore.accounts') || '').split(',')
      : []
  )

  async function generateNewAccount(): Promise<string | null> {
    try {
      const result = await $jsonRpc?.createAccount()
      if (result && result.status === 'success') {
        accounts.value = [...accounts.value, result.data.address]
        currentUserAddress.value = result.data.address
        return result.data.address
      }
      return null
    } catch (error) {
      console.error
      return null
    }
  }
  return { currentUserAddress, accounts, generateNewAccount }
})
