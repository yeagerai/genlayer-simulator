<script setup lang="ts">
import CodeEditor from '@/components/CodeEditor.vue'
import ContractState from '@/components/ContractState.vue'
import NodeLogs from '@/components/NodeLogs.vue'
import ContractOperations from '@/components/ContractOperations.vue'
import { rpcClient } from '@/utils';
import { ref, watch } from 'vue';


const content = ref('');
const contractId = ref<string>();
const abi = ref<any>();
const contractState = ref<any>({});
const defaultStateModalOpen = ref(false);
const defaultContractState = ref('{}');
const showShanckbar = ref(false);
const shanckbarText = ref('');

const handleContentChange = (value: string) => {
  content.value = value;
};

const closeSnackbar = () => {
  showShanckbar.value = false;
  shanckbarText.value = '';
};

const deployContract = async () => {
  const state = JSON.parse(defaultContractState.value || "{}")

  if (Object.keys(state).length < 1) {
    shanckbarText.value = 'You should provide a valid json object as a default state';
    showShanckbar.value = true;
  } else {
    defaultStateModalOpen.value = false;
    closeSnackbar()
    const { result } = await rpcClient.call({
      method: 'deploy_intelligent_contract',
      params: [
        '0xcAE1bEb0daABFc1eF1f4A1C17be7E7b4cc12B33A',
        content.value,
        JSON.stringify(state)
      ]
    })

    contractId.value = result.contract_id;
    defaultContractState.value = "{}"
  }
}

const handleDeployContract = () => {
  defaultStateModalOpen.value = true;
}

const getContractState = async (contractAddress: string) => {
  const { result } = await rpcClient.call({
    method: 'get_contract_state',
    params: [
      contractAddress
    ]
  })
  contractState.value = result.data.state;
}

const handleCallContractMethod = async ({ method, params }: { method: string, params: any[] }) => {
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
  if(contractId.value) {
    getContractState(contractId.value)
  }
}

watch(
  () => contractId.value,
  async (newValue) => {
    if (newValue) {
      if (newValue) {
        await getContractState(newValue);
        const { result } = await rpcClient.call({
          method: 'get_icontract_schema',
          params: [
            newValue
          ]
        })
        abi.value = result
      }
    }
  },
)
</script>

<template>
  <v-container fluid class="m-0 p-0">
    <v-row>
      <v-col>
        <ContractState :contract-state="contractState" />
      </v-col>
      <v-col>
        <CodeEditor :content="content" @deploy="handleDeployContract" @content-change="handleContentChange" />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <ContractOperations :abi="abi" @call-method="handleCallContractMethod" />
      </v-col>
      <v-col>
        <NodeLogs />
      </v-col>
    </v-row>
    <v-dialog v-model="defaultStateModalOpen" width="auto">
      <v-card max-width="600" prepend-icon="mdi-code-json"
        text="Please provide a json object with the default contract state." title="Set the default contrat state">
        <v-container fluid>
          <v-textarea clear-icon="mdi-close-circle" label="State" v-model="defaultContractState" clearable></v-textarea>
        </v-container>
        <template v-slot:actions>
          <v-btn class="ms-auto" @click="deployContract" prepend-icon="mdi-code-greater-than">
            Deploy contract</v-btn>
        </template>
      </v-card>
    </v-dialog>
    <v-snackbar vertical v-model="showShanckbar" multi-line>
      {{ shanckbarText }}

      <template v-slot:actions>
        <v-btn color="red" variant="text" @click="closeSnackbar">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>
