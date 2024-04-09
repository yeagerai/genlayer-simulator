<script setup lang="ts">
import CodeEditor from '@/components/CodeEditor.vue'
import ContractState from '@/components/ContractState.vue'
import NodeLogs from '@/components/NodeLogs.vue'
import ContractOperations from '@/components/ContractOperations.vue'
import { rpcClient } from '@/utils';
import { ref, watch } from 'vue';


const content = ref('');
const contractId = ref<string>();
const abi = ref<string>();
const contractState = ref<any>();

function handleContentChange(value: string) {
  content.value = value;
}

const deployContract = async () => {
  console.log('handle contract deply')
  // deploy the contract code
  const { result } = await rpcClient.call({
    method: 'deploy_intelligent_contract',
    params: [
      '0xcAE1bEb0daABFc1eF1f4A1C17be7E7b4cc12B33A',
      content.value,
      '{}'
    ]
  })

  contractId.value = result.contract_id;
}

const getContractState = async (contractAddress: string) => {
  // deploy the contract code
  const { result } = await rpcClient.call({
    method: 'get_contract_state',
    params: [
      contractAddress
    ]
  })

  contractState.value = result.data.state;
}

watch(
  () => contractId.value,
  async (newValue) => {
    if (newValue) {
      if (newValue) {
        await getContractState(newValue);
        abi.value = await rpcClient.call({
          method: 'get_icontract_schema',
          params: [
            newValue
          ]
        })
      }

    }
  },
)
</script>

<template>
  <v-container fluid class="m-0 p-0">
    <v-row>
      <v-col>
        <ContractState />
      </v-col>
      <v-col>
        <CodeEditor :content="content" @deploy="deployContract" @content-change="handleContentChange" />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <ContractOperations />
      </v-col>
      <v-col>
        <NodeLogs />
      </v-col>
    </v-row>
  </v-container>
</template>
