<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { webSocketClient } from '@/utils'
import { useMainStore } from '@/stores';

const scrollContainer = ref<Element>()


const mainStore = useMainStore()
onMounted(() => {
  webSocketClient.on('status_update', (event) => {
    console.log('webSocketClient.details', event)
    mainStore.nodeLogs.push({ date: new Date().toISOString(), message: event.message })
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
  <div class="z-20 flex flex-col h-full w-full absolute bottom-0 left-0">
    <div class="flex bg-slate-100 p-1 dark:bg-zinc-700 h-6">
    </div>
    <div class="flex flex-col w-full overflow-y-auto h-full p-1 bg-white dark:bg-zinc-800 dark:text-white text-primary cursor-text">
      <div v-if="mainStore.nodeLogs.length > 0"
        class="flex flex-col scroll-smooth overscroll-contain snap-y  snap-start p-0" ref="scrollContainer">
        <div v-for="(item, index) in mainStore.nodeLogs" :key="index" class="flex items-center">
          <div class="flex items-start">
            <div class="flex logs-small-text font-light"><span  class="flex flex-col items-center w-8">{{ index + 1 }}</span> {{ item.date }} :: </div>
            <div class="flex text-xs ml-1 flex-1">{{ item.message }}</div>
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
