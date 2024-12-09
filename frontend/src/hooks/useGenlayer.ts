import { simulator, localNetwork } from 'genlayer-js/chains';
import { createClient, createAccount } from 'genlayer-js';
import type { GenLayerClient } from 'genlayer-js/types';
import { watch } from 'vue';
import { useConfig } from '@/hooks/useConfig';
import { useAccountsStore } from '@/stores';

let client: GenLayerClient<typeof simulator> | null = null;

export function useGenlayer() {
  const accountsStore = useAccountsStore();
  const { isHostedEnvironment } = useConfig();

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
    client = createClient({
      chain: isHostedEnvironment ? simulator : localNetwork,
      account: createAccount(accountsStore.currentPrivateKey || undefined),
    });
  }

  return {
    client,
    initClient,
  };
}
