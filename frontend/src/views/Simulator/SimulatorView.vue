<script setup lang="ts">
import { ref, watch } from 'vue'
import { RouterView } from 'vue-router'
import SimulatorMenu from '@/components/SimulatorMenu.vue'
import NodeLogs from '@/components/Simulator/NodeLogs.vue'
import SimulatorTabs from '@/components/Simulator/SimulatorTabs.vue'
import CodeEditor from '@/components/Simulator/CodeEditor.vue'
import { rpcClient } from '@/utils'
import Modal from '@/components/Modal.vue'

const width = ref(350)

const content = ref('')
const contractId = ref<string>()
const abi = ref<any>()
const contractState = ref<any>({})
const defaultStateModalOpen = ref(false)
const defaultContractState = ref('{}')
const showShanckbar = ref(false)
const shanckbarText = ref('')

const handleContentChange = (value: string) => {
  content.value = value
}

const closeSnackbar = () => {
  showShanckbar.value = false
  shanckbarText.value = ''
}

const deployContract = async () => {
  const state = JSON.parse(defaultContractState.value || '{}')

  if (Object.keys(state).length < 1) {
    shanckbarText.value = 'You should provide a valid json object as a default state'
    showShanckbar.value = true
  } else {
    defaultStateModalOpen.value = false
    closeSnackbar()

    const { result } = await rpcClient.call({
      method: 'deploy_intelligent_contract',
      params: ['0xcAE1bEb0daABFc1eF1f4A1C17be7E7b4cc12B33A', content.value, JSON.stringify(state)]
    })

    contractId.value = result.contract_id
    defaultContractState.value = '{}'
  }
}

const handleDeployContract = () => {
  defaultStateModalOpen.value = true
}

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
</script>

<template>
  <div class="flex">
    <SimulatorMenu />
    <div class="flex">
      <div class="flex p-2 border-r border-r-slate-500" :style="{ width: `${width / 16}rem` }">
        <RouterView />
      </div>
      <div class="flex flex-col relative w-full">
        <div class="flex flex-col m-h-[70%] h-full">
          <SimulatorTabs />
          <CodeEditor :content="content" @deploy="handleDeployContract" @content-change="handleContentChange" />
        </div>
        <NodeLogs />
      </div>
    </div>
    <Modal :open="defaultStateModalOpen" @close="defaultStateModalOpen = false">
      <div class="flex flex-col">
        <div class="flex flex-col">
          <h2>Set the default contrat state</h2>
          <p>Please provide a json object with the default contract state.</p>
        </div>
        <div class="flex">
          <textarea rows="10" class="w-full" v-model="defaultContractState" clear-icon="ri-close-circle"
            label="State" />
        </div>
        <div class="flex justify-end mt-4">
          <button class="bg-primary text-white px-4 py-2 border-r-4" prepend-icon="ri-code-greater-than"
            @click="deployContract">
            Deploy contract
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>
