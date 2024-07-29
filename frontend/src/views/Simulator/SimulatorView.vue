<script setup lang="ts">
import { ref } from 'vue';
import { RouterView } from 'vue-router';
import SimulatorMenu from '@/components/SimulatorMenu.vue';
import NodeLogs from '@/components/Simulator/NodeLogs.vue';
import ContractsPanel from '@/components/Simulator/ContractsPanel.vue';
import { Splitpanes, Pane } from 'splitpanes';
import 'splitpanes/dist/splitpanes.css';

const showLogsTerminal = ref<boolean>(true);

const handleLogsResize = (event: any) => {
  if (event[1]?.size <= 4) {
    showLogsTerminal.value = false;
  } else {
    showLogsTerminal.value = true;
  }
};
</script>

<template>
  <div class="flex w-full">
    <SimulatorMenu />
    <div class="relative flex w-full">
      <Splitpanes
        class="default-theme relative w-full bg-white text-primary dark:bg-zinc-800 dark:text-white"
      >
        <Pane min-size="18" size="18" max-size="60" class="flex w-full">
          <div class="flex w-full overflow-y-auto">
            <RouterView v-slot="{ Component }">
              <KeepAlive>
                <component :is="Component" />
              </KeepAlive>
            </RouterView>
          </div>
        </Pane>
        <Pane>
          <Splitpanes
            class="default-theme"
            horizontal
            @resize="handleLogsResize"
          >
            <Pane
              class="flex h-full w-full flex-col"
              min-size="20"
              size="80"
              max-size="80"
            >
              <ContractsPanel class="h-full w-full" />
            </Pane>
            <Pane
              class="flex w-full flex-col"
              min-size="20"
              :size="20"
              max-size="80"
            >
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
  background-color: transparent;
}

.splitpanes.default-theme .splitpanes__splitter {
  background-color: transparent;
  border-color: #cbd5e1;
  transition: background-color 0.1s;
}

[data-mode='dark'] .splitpanes.default-theme .splitpanes__splitter {
  border-color: #3f3f46 !important;
}

.splitpanes.default-theme .splitpanes__splitter:hover,
.splitpanes.default-theme .splitpanes__splitter:active {
  background-color: #cbd5e1;
}

[data-mode='dark'] .splitpanes.default-theme .splitpanes__splitter:hover,
[data-mode='dark'] .splitpanes.default-theme .splitpanes__splitter:active {
  background-color: #3f3f46;
}

.splitpanes--vertical .splitpanes__splitter {
  min-width: 6px;
  border-left: none !important;
  border-right: 1px solid;
}

.splitpanes--horizontal .splitpanes__splitter {
  z-index: 6 !important;
  /* Avoid having the code editor minimap go over the splitter */
}

.default-theme.splitpanes--horizontal > .splitpanes__splitter:before {
  margin-top: -1px;
}

.default-theme.splitpanes--horizontal > .splitpanes__splitter:after {
  display: none;
}

.default-theme.splitpanes--vertical > .splitpanes__splitter:before {
  display: none;
}

.default-theme.splitpanes--vertical > .splitpanes__splitter:after {
  margin-left: 0;
}

[data-mode='dark'] .splitpanes.default-theme .splitpanes__splitter:before,
[data-mode='dark'] .splitpanes.default-theme .splitpanes__splitter:after {
  background: #313137;
}
</style>
