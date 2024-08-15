import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { getAccountFromPrivatekey, getPrivateKey } from '@/utils';
import type { Address } from '@/types';
import { shortenAddress } from '@/utils';

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
    setCurrentAccount(privateKey);
    return privateKey;
  }

  function accountFromPrivateKey(privateKey: Address) {
    return getAccountFromPrivatekey(privateKey);
  }

  function removeAccount(privateKey: Address) {
    if (privateKeys.value.length <= 1) {
      throw new Error('You need at least 1 account');
    }

    privateKeys.value = privateKeys.value.filter((k) => k !== privateKey);

    if (currentPrivateKey.value === privateKey) {
      setCurrentAccount(privateKeys.value[0] || null);
    }
  }

  function setCurrentAccount(privateKey: Address) {
    currentPrivateKey.value = privateKey;
  }

  const displayAddress = computed(() => {
    try {
      if (!currentPrivateKey.value) {
        return '';
      } else {
        return shortenAddress(
          accountFromPrivateKey(currentPrivateKey.value).address,
        );
      }
    } catch (err) {
      console.error(err);
      return '0x';
    }
  });

  return {
    currentUserAddress,
    currentPrivateKey,
    privateKeys,
    generateNewAccount,
    accountFromPrivateKey,
    removeAccount,
    setCurrentAccount,
    displayAddress,
  };
});
