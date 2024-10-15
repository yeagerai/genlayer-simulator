<script setup lang="ts">
import { useAccountsStore } from '@/stores';
import { notify } from '@kyvg/vue3-notification';
import SimulatorMenu from '@/components/SimulatorMenu.vue';
import AccountItem from '@/components/Simulator/AccountItem.vue';
import MainTitle from '@/components/Simulator/MainTitle.vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { PlusIcon } from '@heroicons/vue/16/solid';
import { useEventTracking } from '@/hooks';

const store = useAccountsStore();
const { trackEvent } = useEventTracking();

const handleCreateNewAccount = async () => {
  const privateKey = store.generateNewAccount();

  if (privateKey) {
    notify({
      title: 'New Account Created',
      type: 'success',
    });

    trackEvent('created_account');
  } else {
    notify({
      title: 'Error creating a new account',
      type: 'error',
    });
  }
};
</script>

<template>
  <div class="flex w-full">
    <SimulatorMenu />

    <div class="relative flex w-full flex-col">
      <MainTitle>Profile</MainTitle>

      <PageSection>
        <template #title>Accounts</template>

        <div class="div mr-auto">
          <div
            class="overflow-hidden rounded-md border border-gray-300 dark:border-gray-800"
          >
            <div class="divide-y divide-gray-200 dark:divide-gray-800">
              <AccountItem
                v-for="privateKey in store.privateKeys"
                :key="privateKey"
                :privateKey="privateKey"
                :active="privateKey === store.currentPrivateKey"
                :canDelete="true"
              />
            </div>
          </div>

          <Btn
            :icon="PlusIcon"
            @click="handleCreateNewAccount"
            class="mt-2 w-full"
          >
            Generate New Address</Btn
          >
        </div>
      </PageSection>
    </div>
  </div>
</template>
