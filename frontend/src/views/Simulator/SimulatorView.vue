<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import SimulatorMenu from '@/components/SimulatorMenu.vue'
import NodeLogs from '@/components/Simulator/NodeLogs.vue'
import ContractsPanel from '@/components/Simulator/ContractsPanel.vue'
import { Splitpanes, Pane } from 'splitpanes'
import 'splitpanes/dist/splitpanes.css'

const minEditorHeight: number = 20
const editorHeight = ref<number>(minEditorHeight)
const editorWidth = ref<number>(15)
const logsHeight = ref<number>(20)
const showLogsTerminal = ref<boolean>(true)

const handleLogsResize = (event: any) => {
  if (event[1]?.size <= 4) {
    showLogsTerminal.value = false
  } else {
    showLogsTerminal.value = true
  }
  
  logsHeight.value = event[1]?.size
  editorHeight.value = event[0]?.size
}
const handlePanelWidthResize = (event: any) => {
  editorWidth.value = event[0]?.size
}

const handleToogleTerminal = () => {
  showLogsTerminal.value = !showLogsTerminal.value
  if (!showLogsTerminal.value) {
    editorHeight.value = 2
  }

}
</script>

<template>
  <div class="flex w-full">
    <SimulatorMenu />
    <div class="flex w-full h-full">
      <Splitpanes class="default-theme w-full h-full bg-white dark:bg-zinc-800 dark:text-white "
        @resize="handlePanelWidthResize">
        <Pane min-size="26" size="26" max-size="60" class="flex w-full">
          <router-view v-slot="{ Component }">
            <keep-alive>
              <component :is="Component" />
            </keep-alive>
          </router-view>
        </Pane>
        <Pane>
          <Splitpanes class="default-theme h-full" horizontal @resize="handleLogsResize">
            <Pane class="flex flex-col relative w-full h-full">
              <div class="flex flex-col h-full w-full">
                <ContractsPanel :parent-height="editorHeight" :parent-width="editorWidth" class="w-full h-full" />
              </div>
            </Pane>
            <Pane class="flex flex-col h-full w-full" min-size="4" :size="logsHeight" max-size="80">
              <NodeLogs :show-terminal="showLogsTerminal" @toggle-terminal="handleToogleTerminal" />
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
  background-color: #cbd5e1 !important;
}
</style>
