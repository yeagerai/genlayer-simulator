import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { getAccountFromPrivatekey, getPrivateKey } from '@/utils'

export const useAccountsStore = defineStore('accountsStore', () => {
  const key = localStorage.getItem('accountsStore.currentPrivateKey')
  const currentPrivateKey = ref<`0x${string}` | null>(key ? (key as `0x${string}`) : null)

  const currentUserAddress = computed(() => {
    return currentPrivateKey.value ? getAccountFromPrivatekey(currentPrivateKey.value).address : ''
  })

  const privateKeys = ref<`0x${string}`[]>(
    localStorage.getItem('accountsStore.privateKeys')
      ? ((localStorage.getItem('accountsStore.privateKeys') || '').split(',') as `0x${string}`[])
      : []
  )

  function generateNewAccount(): `0x${string}` {
    const privateKey = getPrivateKey()
    privateKeys.value = [...privateKeys.value, privateKey]
    currentPrivateKey.value = privateKey
    return privateKey
  }

  function accountFromPrivateKey(privateKey: `0x${string}`) {
    return getAccountFromPrivatekey(privateKey)
  }

  return { currentUserAddress, currentPrivateKey, privateKeys, generateNewAccount, accountFromPrivateKey }
})
