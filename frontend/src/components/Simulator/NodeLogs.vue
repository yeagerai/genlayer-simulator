<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { webSocketClient } from '@/utils'
import { useMainStore } from '@/stores';

const scrollContainer = ref<Element>()
const colorMap: Record<string, string> = {
  'info': 'text-blue-500',
  'error': 'text-red-500',
  'warning': 'text-yellow-500',
  'success': 'text-green-500'
}

const getDataText = (data: any) => {
  if (typeof data !== 'string') return JSON.stringify(data, null, 2)
  return data
}
const mainStore = useMainStore()
onMounted(() => {
  webSocketClient.on('status_update', (event) => {
    console.log('webSocketClient.details', event)
    mainStore.nodeLogs.push(event)
  })
})

watch(mainStore.nodeLogs, () => {
  const scrollTo = scrollContainer.value?.clientHeight || 400
  scrollContainer.value?.scrollTo({ top: scrollTo, behavior: 'smooth' })
})

onUnmounted(() => {
  if (webSocketClient.connected) webSocketClient.close()
})

</script>

<template>
  <div class="z-20 flex flex-col h-full w-full absolute bottom-0 left-0" id="tutorial-node-output">
    <div class="flex flex-col w-full overflow-y-auto h-full p-1 bg-white dark:bg-zinc-800 dark:text-white text-primary cursor-text">
      <div v-if="mainStore.nodeLogs.length > 0"
        class="flex flex-col scroll-smooth overscroll-contain snap-y  snap-start p-0" ref="scrollContainer">
        <div v-for="({ message }, index) in mainStore.nodeLogs" :key="index" class="flex items-center">
          <div class="flex items-start" :class="colorMap[message?.response?.status] || 'text-black-500'">
            
            <div class="flex text-xs font-light"><span class="flex flex-col items-center w-8">{{ index + 1 }}</span> {{
        message.trace_id }} :: </div>
        <div v-if="typeof message === 'string'" class="flex text-xs ml-1 flex-1">"{{ message }}</div>
            <div v-else class="flex text-xs ml-1 flex-1">
              {{ message.function }} {{ message?.response?.message ? ` ===> ${message.response.message}` : '' }}
              || {{ getDataText(message.response?.data || '') }}
            </div>
          </div>
        </div>
      </div>
      <div v-else class="flex flex-col justify-center items-center h-full">
        <div class="flex text-xl">Logs</div>
        <div class="flex">Here you will see every log produced by the simulator</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.logs-small-text {
  font-size: 0.5rem;
}
</style>
