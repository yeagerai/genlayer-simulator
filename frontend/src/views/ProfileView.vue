<script setup lang="ts">
import { useAccountsStore } from '@/stores';
import { notify } from '@kyvg/vue3-notification';
import SimulatorMenu from '@/components/SimulatorMenu.vue';
import { CheckIcon } from '@heroicons/vue/24/solid';
import { ref } from 'vue';

import type { Address } from '@/types';
const store = useAccountsStore();

const showSetDefaultAccount = ref<Record<string, boolean>>({});
const handleCreateNewAccount = async () => {
  const privateKey = store.generateNewAccount();
  if (privateKey) {
    notify({
      title: 'OK',
      text: 'New Account Created',
      type: 'success',
    });
  } else {
    notify({
      title: 'Error',
      text: 'Error creating a new account',
      type: 'error',
    });
  }
};

const handleShowSetDefaultAccount = (privateKey: string) => {
  showSetDefaultAccount.value[privateKey] = true;
};
const handleHideSetDefaultAccount = (privateKey: string) => {
  showSetDefaultAccount.value[privateKey] = false;
};
const setCurentUserAddress = (privateKey: Address) => {
  if (privateKey) {
    store.currentPrivateKey = privateKey;
    showSetDefaultAccount.value = {};
    notify({
      title: 'OK',
      text: 'Default account updated',
      type: 'success',
    });
  }
};
</script>

<template>
  <div class="flex w-full">
    <SimulatorMenu />
    <div class="relative flex w-full">
      <div class="flex flex-col p-4">
        <div class="flex flex-col">
          <h3 class="text-xl">Your Profile</h3>
        </div>
        <div class="flex flex-col py-2">
          <div class="flex flex-col">
            <div class="mt-2 flex flex-col">
              <p class="text-md font-semibold">Your Accounts:</p>
            </div>
            <div class="flex flex-col">
              <div
                class="flex max-h-56 w-full flex-col overflow-y-auto text-xs"
              >
                <div
                  class="flex items-center justify-between p-1 hover:bg-slate-100 dark:bg-zinc-800 dark:hover:bg-zinc-700"
                  v-for="privateKey in store.privateKeys"
                  :key="privateKey"
                >
                  <template v-if="privateKey === store.currentPrivateKey">
                    <div class="flex items-center">
                      <ToolTip
                        text="Your Current Account"
                        :options="{ placement: 'right' }"
                      />
                      <div class="flex pl-4 pr-2 text-primary dark:text-white">
                        {{ store.accountFromPrivateKey(privateKey).address }}
                      </div>
                    </div>
                    <div class="flex h-6 w-6 text-primary dark:text-white">
                      <CheckIcon class="mr-1 h-4 w-4" />
                    </div>
                  </template>
                  <template v-else>
                    <div
                      class="flex cursor-pointer items-center"
                      @click="setCurentUserAddress(privateKey)"
                      @mouseover="handleShowSetDefaultAccount(privateKey)"
                      @mouseleave="handleHideSetDefaultAccount(privateKey)"
                    >
                      <ToolTip
                        text="Set as Current Account"
                        :options="{ placement: 'right' }"
                      />
                      <div class="flex pl-4 pr-2 text-primary dark:text-white">
                        {{ store.accountFromPrivateKey(privateKey).address }}
                      </div>
                    </div>
                    <div class="flex h-6 w-6 text-primary dark:text-white">
                      <CheckIcon
                        v-show="showSetDefaultAccount[privateKey]"
                        class="mr-1 h-4 w-4"
                      />
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-4 flex flex-col">
            <Btn @click="handleCreateNewAccount"> Generate New Address </Btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
