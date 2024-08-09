<script setup lang="ts">
import { nextTick, ref, watch } from 'vue';
import { useNodeStore, useUIStore } from '@/stores';
import JsonViewer from '@/components/JsonViewer/json-viewer.vue';
import GhostBtn from '../global/GhostBtn.vue';
import { NoSymbolIcon, TrashIcon } from '@heroicons/vue/24/solid';
import EmptyListPlaceholder from './EmptyListPlaceholder.vue';

const nodeStore = useNodeStore();
const uiStore = useUIStore();
const scrollContainer = ref<HTMLDivElement>();
const colorMap: Record<string, string> = {
  info: 'text-blue-500',
  error: 'text-red-500',
  warning: 'text-yellow-500',
  success: 'text-green-500',
};

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
      class="flex flex-row items-center justify-between gap-1 border-b bg-white p-1 dark:border-b-zinc-700 dark:bg-zinc-800"
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
        class="relative flex flex-col overflow-y-auto scroll-smooth p-1 pr-8"
        ref="scrollContainer"
      >
        <div
          v-for="({ message, date }, index) in nodeStore.logs"
          :key="index"
          class="flex items-center"
        >
          <div
            class="flex items-start"
            :class="colorMap[message?.response?.status] || 'text-black-500'"
          >
            <div class="flex text-xs font-light">
              <span class="flex w-8 flex-col items-center">{{
                index + 1
              }}</span>
              {{ date }} ::
            </div>
            <div
              v-if="typeof message === 'string'"
              class="ml-1 flex flex-1 text-xs"
            >
              "{{ message }}
            </div>
            <div v-else class="ml-1 flex flex-1 text-xs">
              {{ message.function }}
              {{
                message?.response?.message
                  ? ` ===> ${message.response.message}`
                  : ''
              }}
              <div
                class="ml-2 flex text-xs"
                v-if="typeof message.response?.data === 'string'"
              >
                {{ message.response?.data || '' }}
              </div>
              <JsonViewer
                class="ml-2"
                :value="message.response?.data"
                :theme="uiStore.mode === 'light' ? 'light' : 'dark'"
                :expand="false"
                sort
              />
            </div>
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
