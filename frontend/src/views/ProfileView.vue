<script setup lang="ts">
import { useMainStore } from '@/stores';
import { notify } from "@kyvg/vue3-notification";
import SimulatorMenu from '@/components/SimulatorMenu.vue'
const store = useMainStore()

const handleCreateNewAddress = async () => {
  const address = await store.generateNewAccount()
  if (address) {
    notify({
      title: 'OK',
      text: 'User Address Created',
      type: 'success'
    })
  } else {
    notify({
      title: 'Error',
      text: 'Error creating a new address',
      type: 'error'
    })
  }
}
const setCurentUserAddress = (event: Event) => {
  if((event.target as HTMLSelectElement)?.value) {
    store.currentUserAddress = (event.target as HTMLSelectElement)?.value
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
              <p class="text-md font-semibold">Your Current Address:</p>
              <select class="p-2 w-full bg-slate-100 text-primary overflow-y-auto" @change="setCurentUserAddress"
                :value="store.currentUserAddress">
                <option v-for="account in store.accounts" :key="account" :value="account">
                  {{ account }}
                </option>
              </select>
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
