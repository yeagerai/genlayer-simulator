<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { useNodeStore, useUIStore } from '@/stores'
import JsonViewer from '@/components/JsonViewer/json-viewer.vue'


const nodeStore = useNodeStore()
const uiStore = useUIStore()
const scrollContainer = ref<HTMLDivElement>()
const colorMap: Record<string, string> = {
  'info': 'text-blue-500',
  'error': 'text-red-500',
  'warning': 'text-yellow-500',
  'success': 'text-green-500'
}


watch(nodeStore.logs, () => {
  nextTick(() => {
    scrollContainer.value?.scrollTo({ top: scrollContainer.value.scrollHeight, behavior: 'smooth' })
  })
})
</script>

<template>
  <div class="z-20 flex flex-col h-full w-full absolute bottom-0 left-0">
    <div class="flex bg-slate-100 p-1 dark:bg-zinc-700 h-6">
    </div>
    <div id="tutorial-node-output"
      class="flex flex-col w-full overflow-y-auto h-full p-1 bg-white dark:bg-zinc-800 dark:text-white cursor-text">
      <div v-show="nodeStore.logs.length > 0" class="flex flex-col overflow-y-auto scroll-smooth p-0"
        ref="scrollContainer">
        <div v-for="({ message, date }, index) in nodeStore.logs" :key="index" class="flex items-center">
          <div class="flex items-start" :class="colorMap[message?.response?.status] || 'text-black-500'">

            <div class="flex text-xs font-light"><span class="flex flex-col items-center w-8">{{ index + 1 }}</span> {{
        date }} :: </div>
            <div v-if="typeof message === 'string'" class="flex text-xs ml-1 flex-1">"{{ message }}</div>
            <div v-else class="flex text-xs ml-1 flex-1">
              {{ message.function }} {{ message?.response?.message ? ` ===> ${message.response.message}` : '' }}
              <div class="flex text-xs ml-2" v-if="typeof message.response?.data === 'string'">
                {{ message.response?.data || '' }}
              </div>
              <JsonViewer class="ml-2" :value="message.response?.data"
                :theme="uiStore.mode === 'light' ? 'light' : 'dark'" :expand="false" sort />
            </div>
          </div>
        </div>
      </div>
      <div v-show="nodeStore.logs.length < 1" class="flex flex-col justify-center items-center h-full">
        <div class="flex text-xl">Logs</div>
        <div class="flex">Here you will see every log produced by the simulator</div>
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
