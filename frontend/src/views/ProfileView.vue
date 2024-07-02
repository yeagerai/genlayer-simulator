<script setup lang="ts">
import { useAccountsStore } from '@/stores';
import { notify } from "@kyvg/vue3-notification";
import SimulatorMenu from '@/components/SimulatorMenu.vue'
import { CheckIcon } from '@heroicons/vue/24/solid';
import { ref } from 'vue';
const store = useAccountsStore()

const showSetDefaultAccount = ref<Record<string, boolean>>({})
const handleCreateNewAddress = async () => {
  const address = await store.generateNewAccount()
  if (address) {
    notify({
      title: 'OK',
      text: 'New Account Created',
      type: 'success'
    })
  } else {
    notify({
      title: 'Error',
      text: 'Error creating a new account',
      type: 'error'
    })
  }
}


const handleShowSetDefaultAccount = (address: string) => {
  showSetDefaultAccount.value[address] = true
}
const handleHideSetDefaultAccount = (address: string) => {
  showSetDefaultAccount.value[address] = false
}
const setCurentUserAddress = (address: string) => {
  if (address) {
    store.currentUserAddress = address
    showSetDefaultAccount.value = {}
    notify({
      title: 'OK',
      text: 'Default account updated',
      type: 'success'
    })
  }
}
</script>

<template>
  <div class="flex w-full">
    <SimulatorMenu />
    <div class="flex w-full relative">
      <div class="flex flex-col p-4">
        <div class="flex flex-col">
          <h3 class="text-xl">Your Profile</h3>
        </div>
        <div class="flex flex-col py-2">
          <div class="flex flex-col">
            <div class="flex flex-col mt-2">
              <p class="text-md font-semibold">Your Accounts:</p>
            </div>
            <div class="flex flex-col">
              <div class="flex flex-col text-xs w-full overflow-y-auto max-h-56">
                <div
                  class="flex justify-between items-center hover:bg-slate-100 p-1 dark:bg-zinc-800 dark:hover:bg-zinc-700"
                  v-for="account in store.accounts" :key="account">
                  <template v-if="account === store.currentUserAddress">
                    <div class="flex items-center">
                      <ToolTip text="Your Current Account" :options="{ placement: 'right' }" />
                      <div class="flex  dark:text-white text-primary pl-4 pr-2 ">
                        {{ account }}
                      </div>
                    </div>
                    <div class="flex  dark:text-white text-primary  w-6 h-6">
                      <CheckIcon class="h-4 w-4 mr-1" />
                    </div>
                  </template>
                  <template v-else>
                    <div class="flex items-center cursor-pointer" @click="setCurentUserAddress(account)"
                      @mouseover="handleShowSetDefaultAccount(account)"
                      @mouseleave="handleHideSetDefaultAccount(account)">
                      <ToolTip text="Set as Current Account" :options="{ placement: 'right' }" />
                      <div class="flex  dark:text-white text-primary pl-4 pr-2">
                        {{ account }}
                      </div>
                    </div>
                    <div class="flex  dark:text-white text-primary w-6 h-6">
                      <CheckIcon v-show="showSetDefaultAccount[account]" class="h-4 w-4 mr-1" />
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </div>
          <div class="flex flex-col mt-4">
            <button @click="handleCreateNewAddress"
              class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">Generate New
              Address</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
