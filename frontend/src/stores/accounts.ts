import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { getAccount, getPrivateKey } from '@/utils'

export const useAccountsStore = defineStore('accountsStore', () => {
  const key = localStorage.getItem('accountsStore.currentPrivateKey')
  const currentPrivateKey = ref<`0x${string}` | null>(key ? (key as `0x${string}`) : null)

  const currentUserAddress = computed(() => {
    return currentPrivateKey.value ? getAccount(currentPrivateKey.value).address : ''
  })

  const accounts = ref<`0x${string}`[]>(
    localStorage.getItem('accountsStore.privateKeys')
      ? ((localStorage.getItem('accountsStore.privateKeys') || '').split(',') as `0x${string}`[])
      : []
  )

  function generateNewAccount(): `0x${string}` {
    const privateKey = getPrivateKey()
    accounts.value = [...accounts.value, privateKey]
    currentPrivateKey.value = privateKey
    return privateKey
  }

  function accountFromPrivateKey(privateKey: `0x${string}`) {
    return getAccount(privateKey)
  }

  return { currentUserAddress, currentPrivateKey, accounts, generateNewAccount, accountFromPrivateKey }
})
