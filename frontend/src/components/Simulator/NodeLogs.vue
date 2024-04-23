<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { webSocketClient } from '@/utils'
import { ChevronDoubleDownIcon, ChevronDoubleUpIcon } from '@heroicons/vue/24/solid'
const logs = ref<{ message: string; date: string }[]>([])
const scrollContainer = ref<Element>()
const heigth = ref('h-[25%]') // heigth

onMounted(() => {
  webSocketClient.on('status_update', (event) => {
    console.log('webSocketClient.details', event)
    logs.value.push({ date: new Date().toISOString(), message: event.message })
  })
})

watch(logs.value, () => {
  const scrollTo = scrollContainer.value?.clientHeight || 400
  scrollContainer.value?.scrollTo({ top: scrollTo, behavior: 'smooth' })
})

onUnmounted(() => {
  if (webSocketClient.connected) webSocketClient.close()
})

const toogleTerminal = () => {
  heigth.value = heigth.value === 'h-[25%]' ? 'h-7' : 'h-[25%]'
}


</script>

<template>
  <div class="z-20 flex flex-col h-full w-full absolute bottom-0 left-0">
    <!-- <div class="flex bg-slate-100 p-1 dark:bg-zinc-700">
      <button @click="toogleTerminal" class="ml-2">
        <ChevronDoubleUpIcon class="h-6 w-6 fill-primary" v-if="heigth === 'h-7'" />
        <ChevronDoubleDownIcon class="h-6 w-6 fill-primary" v-else />
        <ToolTip :text="heigth === 'h-7' ? 'Show terminal' : 'Hide terminal'" :options="{ placement: 'top' }" />
      </button>
    </div> -->
    <div class="flex flex-col w-full overflow-y-auto h-full p-1 bg-white dark:bg-zinc-800 dark:text-white cursor-text">
      <dir v-if="logs.length > 0" class="flex flex-col scroll-smooth overscroll-contain snap-y scroll-ml-6 snap-start p-0"
        ref="scrollContainer">
        <div v-for="(item, index) in logs" :key="index" class="flex items-center">
          <div class="flex flex-col items-center w-8">
            <small class="logs-small-text font-light">{{ index + 1 }}</small>
          </div>
          <div class="flex items-center">
            <span class="logs-small-text font-light">{{ item.date }} :: </span>
            <span class="text-xs ml-1">{{ item.message }}</span>
          </div>
        </div>
      </dir>
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
