<script setup>
import { useAccountsStore } from '@/stores';
import AccountItem from '@/components/Simulator/AccountItem.vue';
import { Dropdown } from 'floating-vue';
import { Wallet } from 'lucide-vue-next';

const store = useAccountsStore();
</script>

<template>
  <Dropdown placement="bottom-end">
    <GhostBtn v-tooltip="'Switch account'">
      <Wallet class="h-5 w-5" />
      {{ store.displayAddress }}
    </GhostBtn>

    <template #popper>
      <div class="divide-y divide-gray-200 dark:divide-gray-800">
        <AccountItem
          v-for="privateKey in store.privateKeys"
          :key="privateKey"
          :privateKey="privateKey"
          :active="privateKey === store.currentPrivateKey"
          :canDelete="false"
          v-close-popper
        />
      </div>

      <div
        class="flex w-full border-t border-gray-300 bg-gray-200 p-1 dark:border-gray-600 dark:bg-gray-800"
      >
        <RouterLink :to="{ name: 'profile' }" class="w-full">
          <Btn v-close-popper secondary class="w-full">Manage accounts</Btn>
        </RouterLink>
      </div>
    </template>
  </Dropdown>
</template>
