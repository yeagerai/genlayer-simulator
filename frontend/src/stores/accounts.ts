import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import type { Address } from '@/types';
import { createAccount, generatePrivateKey } from 'genlayer-js';
import type { Account } from 'genlayer-js/types';

export const useAccountsStore = defineStore('accountsStore', () => {
  const key = localStorage.getItem('accountsStore.currentPrivateKey');
  const currentPrivateKey = ref<Address | null>(key ? (key as Address) : null);
  const currentUserAddress = computed(
    () => createAccount(currentPrivateKey.value || undefined).address,
  );

  const privateKeys = ref<Address[]>(
    localStorage.getItem('accountsStore.privateKeys')
      ? ((localStorage.getItem('accountsStore.privateKeys') || '').split(
          ',',
        ) as Address[])
      : [],
  );

  function generateNewAccount(): Address {
    const privateKey = generatePrivateKey();
    privateKeys.value = [...privateKeys.value, privateKey];
    setCurrentAccount(privateKey);
    return privateKey;
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

  function shortenAddress(address?: string) {
    if (!address) {
      return '';
    }

    const maxChars = 4;
    const displayedChars = Math.min(Math.floor(address.length / 3), maxChars);

    return (
      address.slice(0, displayedChars) + '...' + address.slice(-displayedChars)
    );
  }

  // const currentAccount = computed<Account | null>(() => {
  //   if (!currentPrivateKey.value) {
  //     return null;
  //   }
  //   return createAccount(currentPrivateKey.value);
  // });

  const displayAddress = computed(() => {
    try {
      if (!currentPrivateKey.value) {
        return '';
      } else {
        return shortenAddress(createAccount(currentPrivateKey.value).address);
      }
    } catch (err) {
      console.error(err);
      return '0x';
    }
  });

  return {
    // currentAccount,
    currentUserAddress,
    currentPrivateKey,
    privateKeys,
    generateNewAccount,
    removeAccount,
    setCurrentAccount,
    displayAddress,
  };
});
