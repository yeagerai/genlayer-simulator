<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { RouterView } from 'vue-router'
import SimulatorMenu from '@/components/SimulatorMenu.vue'
import NodeLogs from '@/components/Simulator/NodeLogs.vue'
import ContractsPanel from '@/components/Simulator/ContractsPanel.vue'
import { Splitpanes, Pane } from 'splitpanes'
import 'splitpanes/dist/splitpanes.css'

const showLogsTerminal = ref<boolean>(true)
const editorContainerResized = ref<boolean>(false)

const handleLogsResize = (event: any) => {
  editorContainerResized.value = true
  if (event[1]?.size <= 4) {
    showLogsTerminal.value = false
  } else {
    showLogsTerminal.value = true
  }
}

const handlePanelWidthResize = () => {
  editorContainerResized.value = true
}

const resizeEditorHandler = () => {
  editorContainerResized.value = true
}


const handleContractsPanelResize = () => {
  editorContainerResized.value = false
}

onMounted(() => {
  window.addEventListener('resize', resizeEditorHandler)
})
onUnmounted(() => {
  window.removeEventListener('resize', resizeEditorHandler)
})

</script>

<template>
  <div class="flex w-full">
    <SimulatorMenu />
    <div class="flex w-full relative">
      <Splitpanes class="default-theme relative w-full bg-white dark:bg-zinc-800 dark:text-white text-primary "
        @resize="handlePanelWidthResize">
        <Pane min-size="18" size="18" max-size="60" class="flex w-full">
          <div class="overflow-y-auto flex w-full">
            <RouterView v-slot="{ Component }">
              <KeepAlive>
                <component :is="Component" />
              </KeepAlive>
            </RouterView>
          </div>
        </Pane>
        <Pane>
          <Splitpanes class="default-theme" horizontal @resize="handleLogsResize">
            <Pane class="flex flex-col w-full h-full" min-size="20" size="80" max-size="80">
              <ContractsPanel @resized="handleContractsPanelResize" :container-resized="editorContainerResized"
                class="w-full h-full" />
            </Pane>
            <Pane class="flex flex-col w-full" min-size="20" :size="20" max-size="80">
              <NodeLogs />
            </Pane>
          </Splitpanes>
        </Pane>
      </Splitpanes>
    </div>
  </div>
</template>
<style>
.splitpanes__pane {
  display: flex;
  position: relative;
}

.splitpanes.default-theme .splitpanes__pane {
  background-color: transparent !important;
}

.splitpanes.default-theme .splitpanes__splitter {
  background-color: transparent !important;

}

.splitpanes.default-theme .splitpanes__splitter:hover,
.splitpanes.default-theme .splitpanes__splitter:active {
  background-color: #cbd5e1 !important;
}

.splitpanes--vertical>.splitpanes__splitter,
.default-theme .splitpanes--vertical>.splitpanes__splitter {
  border-left: none !important;
  border-right: 1px solid #eee;

}
</style>
