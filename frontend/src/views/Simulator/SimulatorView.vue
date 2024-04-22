<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import SimulatorMenu from '@/components/SimulatorMenu.vue'
import NodeLogs from '@/components/Simulator/NodeLogs.vue'
import ContractsPanel from '@/components/Simulator/ContractsPanel.vue'
import { rpcClient } from '@/utils'

const [minWidth, maxWidth, defaultWidth] = [200, 800, 350]

const width = ref(defaultWidth)
const isResized = ref(false)

const mouseMoveHandler = (e: any) => {
  if (!isResized.value) {
    return;
  }
  const previousWidth = width.value
  const newWidth = previousWidth + e.movementX / 2;

  const isWidthInRange = newWidth >= minWidth && newWidth <= maxWidth;
  width.value = isWidthInRange ? newWidth : previousWidth;
}
const mouseUpHandler = () => {
  isResized.value = false;
}

onMounted(() => {
  window.addEventListener("mousemove", mouseMoveHandler);
  window.addEventListener("mouseup", mouseUpHandler)
})

onUnmounted(() => {
  window.removeEventListener("mousemove", mouseMoveHandler)
  window.removeEventListener("mouseup", mouseUpHandler)
})

const setResized = () => {
  isResized.value = true
}

</script>

<template>
  <div class="flex w-full">
    <SimulatorMenu />
    <div class="flex w-full">
      <div class="flex justify-between" :style="`width: ${width / 16}rem`">
        <RouterView />
        <div className="w-2 border-x bg-slate-100 border-x-slate-500 hover:bg-slate-500 cursor-col-resize dark:bg-zinc-800 dark:text-white" @mousedown="setResized" />
      </div>
      <div class="flex flex-col relative w-full h-full">
        <div class="flex flex-col h-full w-full">
          <ContractsPanel />
        </div>
        <NodeLogs />
      </div>
    </div>

  </div>
</template>
