import { simulator } from 'genlayer-js/chains';
import { createClient, createAccount, generatePrivateKey } from 'genlayer-js';
import type { GenLayerClient, Account } from 'genlayer-js/types';
import { ref, watch } from 'vue';
import { useAccountsStore } from '@/stores';

// TODO: leader only (deploy/write)? Yes, that is only going to work in the local network
let client: GenLayerClient<typeof simulator> | null = null;

export function useGenlayer() {
  console.log('useGenlayer');
  const accountsStore = useAccountsStore();

  if (!client) {
    initClient();
  }

  watch(
    () => accountsStore.currentUserAddress,
    () => {
      initClient();
    },
  );

  function initClient() {
    console.log('- init new client');
    client = createClient({
      chain: simulator,
      account: createAccount(accountsStore.currentPrivateKey || undefined),
    });
    console.log('- client initialized', client);
  }

  return {
    client,
    initClient,
  };
}
