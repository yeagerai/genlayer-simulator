<script setup lang="ts">
import { ref, watch } from 'vue'
import NodeLogs from '../components/NodeLogs.vue'
import CodeEditor from '@/components/CodeEditor.vue'
import ContractState from '@/components/ContractState.vue'
import ContractOperations from '@/components/ContractOperations.vue'
import { rpcClient } from '@/utils'

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
  async (newValue) => {
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
  <VRow class="match-height">
    <VCol cols="12" md="4">
      <ContractState :contract-state="contractState" />
    </VCol>

    <VCol cols="12" md="8">
      <CodeEditor
        :content="content"
        @deploy="handleDeployContract"
        @content-change="handleContentChange"
      />
    </VCol>
    <VCol cols="12" md="4">
      <ContractOperations :abi="abi" @call-method="handleCallContractMethod" />
    </VCol>

    <VCol cols="12" md="8">
      <NodeLogs />
    </VCol>
    <VDialog v-model="defaultStateModalOpen" width="auto">
      <VCard
        max-width="600"
        prepend-icon="mdi-code-json"
        text="Please provide a json object with the default contract state."
        title="Set the default contrat state"
      >
        <VContainer fluid>
          <VTextarea
            v-model="defaultContractState"
            clear-icon="ri-close-circle"
            label="State"
            clearable
          />
        </VContainer>
        <template #actions>
          <VBtn class="ms-auto" prepend-icon="ri-code-greater-than" @click="deployContract">
            Deploy contract
          </VBtn>
        </template>
      </VCard>
    </VDialog>
    <VSnackbar v-model="showShanckbar" vertical multi-line>
      {{ shanckbarText }}

      <template #actions>
        <VBtn color="red" variant="text" @click="closeSnackbar"> Close </VBtn>
      </template>
    </VSnackbar>
  </VRow>
</template>
