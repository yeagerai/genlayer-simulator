import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { getAccountFromPrivatekey, getPrivateKey } from '@/utils';
import type { Address } from '@/types';

export const useAccountsStore = defineStore('accountsStore', () => {
  const key = localStorage.getItem('accountsStore.currentPrivateKey');
  const currentPrivateKey = ref<Address | null>(key ? (key as Address) : null);

  const currentUserAddress = computed(() => {
    return currentPrivateKey.value
      ? getAccountFromPrivatekey(currentPrivateKey.value).address
      : '';
  });

  const privateKeys = ref<Address[]>(
    localStorage.getItem('accountsStore.privateKeys')
      ? ((localStorage.getItem('accountsStore.privateKeys') || '').split(
          ',',
        ) as Address[])
      : [],
  );

  function generateNewAccount(): Address {
    const privateKey = getPrivateKey();
    privateKeys.value = [...privateKeys.value, privateKey];
    currentPrivateKey.value = privateKey;
    return privateKey;
  }

  function accountFromPrivateKey(privateKey: Address) {
    return getAccountFromPrivatekey(privateKey);
  }

  return {
    currentUserAddress,
    currentPrivateKey,
    privateKeys,
    generateNewAccount,
    accountFromPrivateKey,
  };
});
