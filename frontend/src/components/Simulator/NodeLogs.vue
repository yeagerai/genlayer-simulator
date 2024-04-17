<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { webSocketClient } from '@/utils'
import { ChevronDoubleDownIcon, ChevronDoubleUpIcon } from '@heroicons/vue/24/solid'
const logs = ref<{ message: string; date: string }[]>([])
const scrollContainer = ref<Element>()
const heigth = ref('h-[30%]') // heigth

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
  heigth.value = heigth.value === 'h-[30%]' ? 'h-7' : 'h-[30%]'
}


</script>

<template>
  <div class="z-10 flex flex-col w-screen absolute bottom-0 left-0" :class="heigth">
    <div class="flex bg-slate-200 p-1">
      <button @click="toogleTerminal" class="ml-2">
        <ChevronDoubleUpIcon class="h-6 w-6 fill-primary" v-if="heigth === 'h-7'" />
        <ChevronDoubleDownIcon class="h-6 w-6 fill-primary" v-else />
        <ToolTip :text="heigth === 'h-7' ? 'Show terminal' : 'Hide terminal'" :options="{ placement: 'top' }" />
      </button>
    </div>
    <div class="flex flex-col w-full overflow-y-auto h-full bg-white dark:bg-green-950">
      <dir class="flex flex-col scroll-smooth overscroll-contain snap-y scroll-ml-6 snap-start" ref="scrollContainer">
        <div v-for="(item, index) in logs" :key="index" class="flex">
          <div class="mr-3 logs-line-number">
            {{ index + 1 }}
          </div>
          <div class="subtitle">
            <span class="text-xs">{{ item.date }}</span> :: {{ item.message }}
          </div>
        </div>
      </dir>
    </div>
  </div>
</template>

<style scoped>
.logs-line-number {
  font-size: 0.7rem;
}

.item {
  overflow: auto;
  width: 100% !important;
  display: flex;
}

.logs-container {
  background-color: #333333;
  font-family: monospace;
  color: #f2f2f2;
}

.subtitle {
  font-size: 0.7rem;
}
</style>
