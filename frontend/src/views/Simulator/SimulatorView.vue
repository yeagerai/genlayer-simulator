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

const contractId = ref<string>()
const abi = ref<any>()
const contractState = ref<any>({})
const showShanckbar = ref(false)
const shanckbarText = ref('')


const getContractState = async (contractAddress: string) => {
  const { result } = await rpcClient.call({
    method: 'get_contract_state',
    params: [contractAddress]
  })

  contractState.value = result.data.state
}

const handleCallContractMethod = async ({ method, params }: { method: string; params: any[] }) => {
  const result = await rpcClient.call({
    method: 'call_contract_function',
    params: [
      contractId.value, // TODO: replace with a current account
      contractId.value,
      `${abi.value.class}.${method}`,
      params
    ]
  })

  console.log('handleCallContractMethod', result)
  if (contractId.value) getContractState(contractId.value)
}

watch(
  () => contractId.value,
  async (newValue: any): Promise<void> => {
    if (newValue) {
      if (newValue) {
        await getContractState(newValue)

        const { result } = await rpcClient.call({
          method: 'get_icontract_schema',
          params: [newValue]
        })

        abi.value = result
      }
    }
  }
)
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
        <div class="flex flex-col h-full w-full overflow-y-auto">
          <ContractsPanel />
        </div>
        <NodeLogs />
      </div>
    </div>

  </div>
</template>
