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

  logsHeight.value = event[1]?.size < 2 ? 4 : event[1]?.size
  editorHeight.value = event[0]?.size < minEditorHeight ? minEditorHeight : event[0]?.size
  
}
const handlePanelWidthResize = (event: any) => {
  editorWidth.value = event[0]?.size
}

const handleToogleTerminal = () => {
  showLogsTerminal.value = !showLogsTerminal.value
  if (!showLogsTerminal.value) {
    editorHeight.value = 2
  } else {
    editorHeight.value = 20
  }

}
</script>

<template>
  <div class="flex w-full">
    <SimulatorMenu />
    <div class="flex w-full relative">
      <Splitpanes class="default-theme relative w-full bg-white dark:bg-zinc-800 dark:text-white "
        @resize="handlePanelWidthResize">
        <Pane min-size="18" size="18" max-size="60" class="flex w-full">
          <div class="overflow-y-auto flex w-full">
            <router-view v-slot="{ Component }">
            <keep-alive>
              <component :is="Component" />
            </keep-alive>
          </router-view>
          </div>
        </Pane>
        <Pane>
          <Splitpanes class="default-theme" horizontal @resize="handleLogsResize">
            <Pane class="flex flex-col w-full h-full" min-size="20" size="80" max-size="80">
              <div class="flex flex-col h-full w-full">
                <ContractsPanel :parent-height="editorHeight" :parent-width="editorWidth" class="w-full h-full" />
              </div>
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
  background-color: #cbd5e1 !important;
}
</style>
