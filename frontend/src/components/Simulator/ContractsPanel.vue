<script setup lang="ts">
import { PlayIcon } from '@heroicons/vue/24/solid';
import ContractTab from '@/components/Simulator/ContractTab.vue';
import CodeEditor from '@/components/Simulator/CodeEditor.vue';
import { useContractsStore } from '@/stores';
import { computed } from 'vue';
import HomeTab from './HomeTab.vue';
import { useRouter } from 'vue-router';

const store = useContractsStore();
const router = useRouter();

const handleRunDebug = () => {
  router.push({ name: 'run-debug' });
};

const setCurrentContractTab = (id?: string) => {
  console.log(' setCurrentContractTab', id);
  store.setCurrentContractId(id);
};

const handleCloseContract = (id?: string) => {
  store.closeFile(id || '');
};

const contracts = computed(() => {
  return store.contracts.filter((contract) =>
    store.openedFiles.includes(contract.id || ''),
  );
});

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
          @selectContract="setCurrentContractTab('')"
        />

        <ContractTab
          v-for="contract in contracts"
          :key="contract.id"
          :contract="contract"
          class="contract-item"
          :id="`contract-item-${contract.id}`"
          :isActive="contract.id === store.currentContractId"
          @closeContract="handleCloseContract(contract.id)"
          @selectContract="setCurrentContractTab(contract.id)"
        />
      </div>
      <div class="mr-3 flex p-2">
        <button class="ml-3 flex" @click="handleRunDebug">
          <PlayIcon class="h-5 w-5 fill-primary dark:fill-white" />
          <ToolTip text="Run and Debug" :options="{ placement: 'bottom' }" />
        </button>
      </div>
    </nav>
    <div v-show="showHome" class="flex h-full w-full">
      <HomeTab />
    </div>
    <div
      v-for="contract in contracts"
      :key="contract.id"
      class="relative flex h-full w-full"
      v-show="contract.id === store.currentContractId"
    >
      <CodeEditor :contract="contract" @run-debug="handleRunDebug" />
    </div>
  </div>
</template>
