<script setup lang="ts">
import { PlayIcon } from '@heroicons/vue/24/solid';
import ContractTab from '@/components/Simulator/ContractTab.vue';
import CodeEditor from '@/components/Simulator/CodeEditor.vue';
import { useContractsStore } from '@/stores';
import { computed } from 'vue';
import HomeTab from './HomeTab.vue';
import { useRouter, useRoute } from 'vue-router';
import { useContractQueries } from '@/hooks';

const store = useContractsStore();
const router = useRouter();
const route = useRoute();
const { contractSchemaQuery } = useContractQueries();
const { error } = contractSchemaQuery;

const handleRunDebug = () => {
  router.push({ name: 'run-debug' });
};

const showHome = computed(() => store.currentContractId === '');

const handleHorizontalScroll = (event: WheelEvent) => {
  if (!event.shiftKey && event.currentTarget instanceof HTMLElement) {
    event.preventDefault();
    event.currentTarget.scrollLeft += event.deltaY;
  }
};
</script>

<template>
  <div class="flex h-full w-full flex-col">
    <nav
      class="flex items-stretch justify-between border-b text-sm dark:border-zinc-700"
    >
      <div
        class="no-scrollbar flex items-stretch justify-start overflow-x-auto"
        @wheel.stop="handleHorizontalScroll"
      >
        <ContractTab
          id="tutorial-welcome"
          :isHomeTab="true"
          :isActive="showHome"
          @selectContract="store.setCurrentContractId('')"
        />

        <ContractTab
          v-for="contract in store.openedFiles"
          :key="contract.id"
          :contract="contract"
          class="contract-item"
          :id="`contract-item-${contract.id}`"
          :isActive="contract.id === store.currentContractId"
          @closeContract="store.closeFile(contract.id)"
          @selectContract="store.openFile(contract.id)"
        />
      </div>

      <div>
        <Btn
          v-if="route.name !== 'run-debug' && store.currentContractId"
          class="m-1 flex items-center !p-1"
          @click="handleRunDebug"
          v-tooltip="'Run and Debug'"
        >
          <PlayIcon class="h-5 w-5" />
        </Btn>
      </div>
    </nav>

    <HomeTab v-show="showHome" />

    <div
      v-if="!!error"
      class="left-O right-O absolute bottom-0 z-10 w-full bg-red-500 px-2 py-1 text-sm text-white"
    >
      {{ error }}
    </div>

    <div
      v-for="contract in store.contracts"
      :key="contract.id"
      class="relative flex h-full w-full"
      v-show="contract.id === store.currentContractId"
    >
      <CodeEditor :contract="contract" @run-debug="handleRunDebug" />
    </div>
  </div>
</template>
