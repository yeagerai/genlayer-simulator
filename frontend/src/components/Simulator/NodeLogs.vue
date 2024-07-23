<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { useNodeStore, useUIStore } from '@/stores'
import JsonViewer from '@/components/JsonViewer/json-viewer.vue'

const nodeStore = useNodeStore()
const uiStore = useUIStore()
const scrollContainer = ref<HTMLDivElement>()
const colorMap: Record<string, string> = {
  info: 'text-blue-500',
  error: 'text-red-500',
  warning: 'text-yellow-500',
  success: 'text-green-500',
}

watch(nodeStore.logs, () => {
  nextTick(() => {
    scrollContainer.value?.scrollTo({
      top: scrollContainer.value.scrollHeight,
      behavior: 'smooth',
    })
  })
})
</script>

<template>
  <div class="absolute bottom-0 left-0 z-20 flex h-full w-full flex-col">
    <div
      id="tutorial-node-output"
      class="flex h-full w-full cursor-text flex-col overflow-y-auto bg-white p-1 dark:bg-zinc-800 dark:text-white"
    >
      <div
        v-show="nodeStore.logs.length > 0"
        class="flex flex-col overflow-y-auto scroll-smooth p-0"
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
        class="flex h-full flex-col items-center justify-center"
      >
        <div class="flex text-xl">Logs</div>
        <div class="flex">
          Here you will see every log produced by the simulator
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
