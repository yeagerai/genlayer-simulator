<script setup>
import { useAccountsStore } from '@/stores';
import AccountItem from '@/components/Simulator/AccountItem.vue';
import { Dropdown } from 'floating-vue';
import { shortenAddress } from '@/utils';
import { Wallet } from 'lucide-vue-next';

const store = useAccountsStore();
</script>

<template>
  <Dropdown placement="bottom-end">
    <GhostBtn v-tooltip="'Switch account'">
      <Wallet class="h-5 w-5" />
      {{
        shortenAddress(
          store.accountFromPrivateKey(store.currentPrivateKey).address,
        )
      }}
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

<style>
[data-mode='dark'] .v-popper--theme-dropdown .v-popper__inner {
  color: inherit;
  padding: 0px;
  border: 1px solid #4b5563;
  background: none;
}
</style>
