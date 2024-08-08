import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { getAccountFromPrivatekey, getPrivateKey } from '@/utils';
import { shortenAddress } from '@/utils';

export const useAccountsStore = defineStore('accountsStore', () => {
  const key = localStorage.getItem('accountsStore.currentPrivateKey');
  const currentPrivateKey = ref<`0x${string}` | null>(
    key ? (key as `0x${string}`) : null,
  );

  const currentUserAddress = computed(() => {
    return currentPrivateKey.value
      ? getAccountFromPrivatekey(currentPrivateKey.value).address
      : '';
  });

  const privateKeys = ref<`0x${string}`[]>(
    localStorage.getItem('accountsStore.privateKeys')
      ? ((localStorage.getItem('accountsStore.privateKeys') || '').split(
          ',',
        ) as `0x${string}`[])
      : [],
  );

  function generateNewAccount(): `0x${string}` {
    const privateKey = getPrivateKey();
    privateKeys.value = [...privateKeys.value, privateKey];
    setCurrentAccount(privateKey);
    return privateKey;
  }

  function accountFromPrivateKey(privateKey: `0x${string}`) {
    return getAccountFromPrivatekey(privateKey);
  }

  function removeAccount(privateKey: `0x${string}`) {
    privateKeys.value = privateKeys.value.filter((k) => k !== privateKey);

    if (currentPrivateKey.value === privateKey) {
      setCurrentAccount(privateKeys.value[0] || null);
    }
  }

  function setCurrentAccount(privateKey: `0x${string}`) {
    currentPrivateKey.value = privateKey;
  }

  const displayAddress = computed(() => {
    if (!currentPrivateKey.value) {
      return '';
    } else {
      return shortenAddress(
        accountFromPrivateKey(currentPrivateKey.value).address,
      );
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
