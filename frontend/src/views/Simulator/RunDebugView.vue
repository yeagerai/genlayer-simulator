<script setup lang="ts">
import { useContractsFilesStore } from "@/stores"
import { computed, ref, watch } from "vue";
import { rpcClient } from '@/utils';
import { notify } from "@kyvg/vue3-notification";
import ContractState from '@/components/Simulator/ContractState.vue'
import ExecuteTransactions from "@/components/Simulator/ExecuteTransactions.vue";
import TransactionsList from "@/components/Simulator/TransactionsList.vue";

const store = useContractsFilesStore()
const defaultContractState = ref('{}')
const abi = ref<any>()
const contractState = ref<any>({})
const contract = computed(() => store.contracts.find(contract => contract.id === store.currentContractId))
const deployedContract = computed(() => store.deployedContracts.find(contract => contract.contractId === store.currentContractId))
const contractTransactions = ref<any[]>([])

const getContractState = async (contractAddress: string) => {
  const { result } = await rpcClient.call({
    method: 'get_contract_state',
    params: [contractAddress]
  })

  contractState.value = result.data.state
}

const handleCallContractMethod = async ({ method, params }: { method: string; params: any[] }) => {
  console.log('handleCallContractMethod', method, params, abi.value.class)
  const result = await rpcClient.call({
    method: 'call_contract_function',
    params: [
      deployedContract.value?.address, // TODO: replace with a current account
      deployedContract.value?.address,
      `${abi.value.class}.${method}`,
      params
    ]
  })

  console.log('handleCallContractMethod', result)
  contractTransactions.value.push(result)
  if (deployedContract.value?.address) getContractState(deployedContract.value?.address)
}

const handleDeployContract = async () => {
  const defaultState = JSON.parse(defaultContractState.value || '{}')
  const contract = store.contracts.find(c => c.id === store.currentContractId)
  if (contract) {
    if (Object.keys(defaultState).length < 1) {
      notify({
        title: 'Error',
        text: 'You should provide a valid json object as a default state',
        type: 'error'
      })
    } else {

      const { result } = await rpcClient.call({
        method: 'deploy_intelligent_contract',
        params: ['0xcAE1bEb0daABFc1eF1f4A1C17be7E7b4cc12B33A', contract.content, JSON.stringify(defaultState)]
      })

      store.addDeployedContract({ address: result.contract_id, contractId: contract.id })
      defaultContractState.value = '{}'
      notify({
        title: 'OK',
        text: 'Contract deployed',
        type: 'success'
      })
    }
  }

}

watch(
  () => deployedContract.value,
  async (newValue: any): Promise<void> => {
    if (newValue) {
      if (newValue) {
        await getContractState(newValue.address)

        const { result } = await rpcClient.call({
          method: 'get_icontract_schema',
          params: [newValue.address]
        })

        abi.value = result
      }
    }
  }
)
</script>

<template>
  <div class="flex flex-col w-full overflow-y-auto">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Run and Debug</h3>
    </div>
    <template v-if="!!store.currentContractId">
      <div class="flex flex-col px-2 py-2 w-full bg-slate-100">
        <div class="text-sm">Intelligent Contract:</div>
        <div class="text-xs text-neutral-800">
          {{ contract?.name }}.gpy
        </div>
      </div>
      <div class="flex flex-col p-2 my-4">
        <div class="flex flex-col text-xs">
          <h2>Set the default contrat state</h2>
          <p>Please provide a json object with the default contract state.</p>
        </div>
        <div class="flex mt-2">
          <textarea rows="5" class="w-full bg-slate-100 dark:dark:bg-zinc-700 p-2" v-model="defaultContractState"
            clear-icon="ri-close-circle" label="State" />
        </div>
      </div>
      <div class="flex flex-col p-2 w-full justify-center">
        <ToolTip text="Deploy" :options="{ placement: 'top' }" />
        <button @click="handleDeployContract"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">Deploy Intelligent
          Contract</button>
      </div>

      <template v-if="deployedContract">
        <ContractState :contract-state="contractState" :deployed-contract="deployedContract"/>

      <ExecuteTransactions :abi="abi" @call-method="handleCallContractMethod"/>
      <TransactionsList :transactions="contractTransactions" />
      </template>
    </template>
    <div class="flex flex-col px-2 py-2 w-full bg-slate-100" v-else>
      <div class="text-sm">Please select an intelligent contract first, you can go to <RouterLink
          :to="{ name: 'simulator.contracts' }" class="text-primary">

          Files llist.
        </RouterLink>
      </div>
    </div>
  </div>
</template>
