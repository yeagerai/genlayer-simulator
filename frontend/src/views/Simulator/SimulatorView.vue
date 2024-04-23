<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import SimulatorMenu from '@/components/SimulatorMenu.vue'
import NodeLogs from '@/components/Simulator/NodeLogs.vue'
import ContractsPanel from '@/components/Simulator/ContractsPanel.vue'
import { Splitpanes, Pane } from 'splitpanes'
import 'splitpanes/dist/splitpanes.css'

const minEditorHeight: number = 10
const editorHeight = ref<number>(minEditorHeight)
const editorWidth = ref<number>(15)

const handleLogsResize = (event: any) => {
  editorHeight.value = event[0]?.size
}
const handlePanelWidthResize = (event: any) => {
  editorWidth.value = event[0]?.size
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
            <Pane min-size="20" size="80" max-size="80" class="flex flex-col relative w-full h-full">
              <div class="flex flex-col h-full w-full">
                <ContractsPanel :parent-height="editorHeight" :parent-width="editorWidth" class="w-full h-full" />
              </div>
            </Pane>
            <Pane class="flex flex-col h-full w-full">
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

</style>
