<script setup lang="ts">
import { nextTick, ref, watch, computed, type ComputedRef } from 'vue';
import { useNodeStore, useUIStore } from '@/stores';
import JsonViewer from '@/components/JsonViewer/json-viewer.vue';
import GhostBtn from '../global/GhostBtn.vue';
import EmptyListPlaceholder from './EmptyListPlaceholder.vue';
import { Ban } from 'lucide-vue-next';
import LogFilterBtn from '@/components/Simulator/LogFilterBtn.vue';

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

const categories = ref(['RPC', 'GenVM', 'Consensus', 'Transactions']);
const statuses = ref(['info', 'error', 'warning', 'success']);

const selectedCategories = ref(categories.value);
const selectedStatuses = ref(['info', 'error', 'warning', 'success']);

const toggleCategory = (category: string) => {
  if (selectedCategories.value.includes(category)) {
    selectedCategories.value = selectedCategories.value.filter(
      (c) => c !== category,
    );
  } else {
    selectedCategories.value.push(category);
  }
};

const toggleStatus = (status: string) => {
  if (selectedStatuses.value.includes(status)) {
    selectedStatuses.value = selectedStatuses.value.filter((s) => s !== status);
  } else {
    selectedStatuses.value.push(status);
  }
};

const filteredLogs = computed(() => {
  return nodeStore.logs.filter((log) => {
    const categoryMatch =
      selectedCategories.value.length === 0 ||
      selectedCategories.value.includes(log.category);
    const statusMatch =
      selectedStatuses.value.length === 0 ||
      selectedStatuses.value.includes(log.type);
    return categoryMatch && statusMatch;
  });
});

const isAnyFilterActive = computed(() => {
  return (
    selectedCategories.value.length !== categories.value.length ||
    selectedStatuses.value.length !== statuses.value.length
  );
});

const resetFilters = () => {
  selectedCategories.value = categories.value;
  selectedStatuses.value = statuses.value;
};
</script>

<template>
  <div class="flex h-full w-full flex-col">
    <div
      class="flex flex-row items-center justify-between gap-1 border-b bg-white p-1 pl-2 dark:border-b-zinc-700 dark:bg-zinc-800"
    >
      Logs

      <div class="flex flex-row items-center gap-1">
        <div class="flex flex-row items-center gap-1">
          <span class="font-mono text-xs opacity-50">Category</span>
          <LogFilterBtn
            v-for="category in categories"
            :key="category"
            :active="selectedCategories.includes(category)"
            @click="toggleCategory(category)"
          >
            {{ category }}
          </LogFilterBtn>
        </div>

        <div class="flex flex-row items-center gap-1">
          <span class="font-mono text-xs opacity-50">Status</span>
          <LogFilterBtn
            v-for="status in statuses"
            :key="status"
            :active="selectedStatuses.includes(status)"
            @click="toggleStatus(status)"
          >
            {{ status }}
          </LogFilterBtn>
        </div>

        <GhostBtn
          @click="nodeStore.clearLogs"
          v-tooltip="{ content: 'Clear Logs', placement: 'left' }"
          class="opacity-50"
        >
          <Ban :size="14" />
        </GhostBtn>
      </div>
    </div>

    <div
      id="tutorial-node-output"
      class="flex h-full w-full cursor-text flex-col overflow-y-auto bg-slate-50 dark:bg-zinc-900"
    >
      <div
        v-show="filteredLogs.length > 0"
        class="relative flex flex-col overflow-y-auto scroll-smooth"
        ref="scrollContainer"
      >
        <div
          v-for="(
            { category, event, type, message, data }, index
          ) in filteredLogs"
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
        v-show="filteredLogs.length < 1"
        class="grid h-full w-full place-items-center"
      >
        <div>
          <EmptyListPlaceholder>
            No logs found.
            <button
              v-if="isAnyFilterActive"
              class="text-center underline"
              @click="resetFilters"
            >
              Reset filters
            </button>
          </EmptyListPlaceholder>
        </div>
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
