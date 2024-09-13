<script setup lang="ts">
import { nextTick, ref, watch, computed, type ComputedRef } from 'vue';
import { useNodeStore, useUIStore } from '@/stores';
import JsonViewer from '@/components/JsonViewer/json-viewer.vue';
import GhostBtn from '../global/GhostBtn.vue';
import { NoSymbolIcon } from '@heroicons/vue/24/solid';
import EmptyListPlaceholder from './EmptyListPlaceholder.vue';

const nodeStore = useNodeStore();
const uiStore = useUIStore();
const scrollContainer = ref<HTMLDivElement>();

type ColorMapType = {
  [key: string]: string; // Add index signature
};
const colorMap: ComputedRef<ColorMapType> = computed(() => ({
  // contractLog: uiStore.mode === 'light' ? 'text-black' : 'text-white',
  info: 'text-blue-400',
  error: 'text-red-400',
  warning: 'text-yellow-400',
  success: 'text-green-400',
}));

watch(nodeStore.logs, () => {
  nextTick(() => {
    scrollContainer.value?.scrollTo({
      top: scrollContainer.value.scrollHeight,
      behavior: 'smooth',
    });
  });
});
</script>

<template>
  <div class="flex h-full w-full flex-col">
    <div
      class="flex flex-row items-center justify-between gap-1 border-b bg-white p-1 pl-2 dark:border-b-zinc-700 dark:bg-zinc-800"
    >
      Logs
      <GhostBtn
        @click="nodeStore.clearLogs"
        v-tooltip="{ content: 'Clear Logs', placement: 'left' }"
        class="opacity-50"
      >
        <NoSymbolIcon class="h-4 w-4" />
      </GhostBtn>
    </div>

    <div
      id="tutorial-node-output"
      class="flex h-full w-full cursor-text flex-col overflow-y-auto bg-slate-50 dark:bg-zinc-900"
    >
      <div
        v-show="nodeStore.logs.length > 0"
        class="relative flex flex-col overflow-y-auto scroll-smooth"
        ref="scrollContainer"
      >
        <div
          v-for="(
            { category, event, type, message, data }, index
          ) in nodeStore.logs"
          :key="index"
          class="flex flex-row border-b border-gray-200 px-1 py-1 font-mono text-[10px] first-line:items-center dark:border-zinc-800"
        >
          <div class="flex flex-row gap-1">
            <div class="rounded bg-gray-800 px-[3px] py-[1px]">
              {{ category }}
            </div>

            <div
              class="rounded bg-gray-800 px-[3px] py-[1px]"
              :class="colorMap[type]"
            >
              {{ event }}
            </div>

            <div :class="colorMap[type]">
              {{ message }}
            </div>

            <JsonViewer
              class="ml-2"
              v-if="data"
              :value="data"
              :theme="uiStore.mode === 'light' ? 'light' : 'dark'"
              :expand="false"
              sort
            />
          </div>
        </div>
      </div>

      <div
        v-show="nodeStore.logs.length < 1"
        class="grid h-full w-full place-items-center"
      >
        <EmptyListPlaceholder> No logs found. </EmptyListPlaceholder>
      </div>
    </div>
  </div>
</template>

<style>
.jv-code {
  padding: 0 !important;
}

.logs-small-text {
  font-size: 0.5rem;
}
</style>
