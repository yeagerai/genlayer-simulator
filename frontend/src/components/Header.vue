<script setup lang="ts">
import { PresentationChartLineIcon } from '@heroicons/vue/24/solid';
import { SunIcon, MoonIcon } from '@heroicons/vue/16/solid';
import { useUIStore, useAccountsStore } from '@/stores';
import { shortenAddress } from '@/utils';
import { RouterLink } from 'vue-router';
import Logo from '@/assets/images/logo.svg';
import GhostBtn from './global/GhostBtn.vue';

const uiStore = useUIStore();
const accounts = useAccountsStore();
const toggleMode = () => {
  uiStore.toggleMode();
};
const showTutorial = () => {
  uiStore.runTutorial();
};
</script>

<template>
  <header
    class="flex items-center justify-between border-b border-b-slate-500 p-2 dark:border-b-zinc-500 dark:bg-zinc-800"
  >
    <RouterLink to="/">
      <Logo
        alt="GenLayer Logo"
        height="36"
        :class="[
          'block',
          uiStore.mode === 'light' ? 'text-primary' : 'text-white',
        ]"
      />
    </RouterLink>

    <div class="flex items-center gap-2 pr-2" id="tutorial-end">
      <RouterLink :to="{ name: 'profile' }">
        <GhostBtn class="px-2">
          {{ shortenAddress(accounts.currentUserAddress || '') }}
        </GhostBtn>

        <ToolTip
          :text="accounts.currentUserAddress"
          :options="{ placement: 'bottom' }"
        />
      </RouterLink>

      <GhostBtn @click="toggleMode">
        <SunIcon v-if="uiStore.mode === 'light'" class="h-5 w-5" />
        <MoonIcon v-else class="h-5 w-5 fill-gray-200" />
        <ToolTip text="Switch Theme" :options="{ placement: 'bottom' }" />
      </GhostBtn>

      <GhostBtn @click="showTutorial">
        <PresentationChartLineIcon
          class="h-5 w-5"
          :class="uiStore.mode === 'light' ? 'fill-gray-700' : 'fill-gray-200'"
        />
        <ToolTip text="Show Tutorial" :options="{ placement: 'bottom' }" />
      </GhostBtn>
    </div>
  </header>
</template>
