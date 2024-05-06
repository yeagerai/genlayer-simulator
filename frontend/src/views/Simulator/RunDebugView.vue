<script setup lang="ts">
import { useMainStore } from '@/stores'
import { computed, onMounted, ref, watch } from 'vue'
import { rpcClient } from '@/utils'
import { notify } from '@kyvg/vue3-notification'
import ContractState from '@/components/Simulator/ContractState.vue'
import ExecuteTransactions from '@/components/Simulator/ExecuteTransactions.vue'
import TransactionsList from '@/components/Simulator/TransactionsList.vue'
import type { DeployedContract } from '@/types'
import { type } from 'os'

const store = useMainStore()
const contractContructorParams = ref('{}')
const abi = ref<any>()
const contractState = ref<any>({})
const contract = computed(() =>
  store.contracts.find((contract) => contract.id === store.currentContractId)
)
const deployedContract = computed(() =>
  store.deployedContracts.find((contract) => contract.contractId === store.currentContractId)
)
const contractTransactions = ref<any[]>([])

const handleGetContractState = async (contractAddress: string, method: string) => {
  const { result } = await rpcClient.call({
    method: 'get_contract_state',
    params: [contractAddress, method]
  })

  contractState.value = {
    ...contractState.value,
    [method]: result.data.result
  }
}

const handleCallContractMethod = async ({ method, params }: { method: string; params: any[] }) => {
  console.log('handleCallContractMethod', method, params, abi.value.class)
  const { result } = await rpcClient.call({
    method: 'call_contract_function',
    params: [
      store.currentUserAddress,
      deployedContract.value?.address,
      `${abi.value.class}.${method}`,
      params
    ]
  })

  contractTransactions.value.push(result)
}

const handleDeployContract = async () => {
  const constructorParams = JSON.parse(contractContructorParams.value || '{}')
  const contract = store.contracts.find((c) => c.id === store.currentContractId)
  if (contract) {
    if (Object.keys(constructorParams).length < 1) {
      notify({
        title: 'Error',
        text: 'You should provide a valid json object as a default state',
        type: 'error'
      })
    } else {
      // Getting the ABI to check the class name
      const { result: { data: contractSchema } } = await rpcClient.call({
        method: 'get_icontract_schema_for_code',
        params: [contract.content]
      })

      // Deploy the contract
      const constructorParamsAsString = JSON.stringify(constructorParams, null, 2)
      const { result } = await rpcClient.call({
        method: 'deploy_intelligent_contract',
        params: [
          store.currentUserAddress,
          contractSchema.class,
          contract.content,
          constructorParamsAsString
        ]
      })

      if (result?.status === 'success') {
        store.addDeployedContract({
          address: result?.data.contract_id,
          contractId: contract.id,
          defaultState: constructorParamsAsString
        })
        notify({
          title: 'OK',
          text: 'Contract deployed',
          type: 'success'
        })
      } else {
        notify({
          title: 'Error',
          text: typeof result.message === 'string' ? result.message : 'Error Deploying the contract',
          type: 'error'
        })
      }
    }
  }
}

const setDefaultState = async (contract: DeployedContract) => {
  try {
    contractContructorParams.value = contract.defaultState

    const { result } = await rpcClient.call({
      method: 'get_icontract_schema',
      params: [contract.address]
    })

    abi.value = result.data
  } catch (error) {
    console.error(error)
    store.removeDeployedContract(contract.contractId)
  }
}

watch(deployedContract, (newValue) => {
  if (newValue) {
    setDefaultState(newValue)
  }
})

onMounted(() => {
  if (deployedContract.value) setDefaultState(deployedContract.value)
})
</script>

<template>
  <div class="flex flex-col w-full overflow-y-auto max-h-[93vh]">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Run and Debug</h3>
    </div>
    <div class="flex flex-col overflow-y-auto" v-if="!!store.currentContractId">
      <div class="flex flex-col">
        <div class="flex flex-col px-2 py-2 w-full bg-slate-100">
          <div class="text-sm">Intelligent Contract:</div>
          <div class="text-xs text-neutral-800">
            {{ contract?.name }}
          </div>
        </div>
        <div class="flex flex-col p-2 my-4">
          <div class="flex flex-col text-xs">
            <h2>Constructor Parameters</h2>
            <p>Please provide a json object with the constructor parameters.</p>
          </div>
          <div class="flex mt-2">
            <textarea rows="5" class="w-full bg-slate-100 dark:dark:bg-zinc-700 p-2" v-model="contractContructorParams"
              clear-icon="ri-close-circle" label="State" />
          </div>
        </div>
        <div class="flex flex-col p-2 w-full justify-center">
          <ToolTip text="Deploy" :options="{ placement: 'top' }" />
          <button @click="handleDeployContract"
            class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
            Deploy
          </button>
        </div>
      </div>
      <div class="flex flex-col" v-if="deployedContract">
        <div class="flex flex-col">
          <ContractState :abi="abi" :contract-state="contractState" :deployed-contract="deployedContract"
            :get-contract-state="handleGetContractState" />
        </div>

        <div class="flex flex-col">
          <ExecuteTransactions :abi="abi" @call-method="handleCallContractMethod" />
        </div>
        <div class="flex flex-col">
          <TransactionsList :transactions="contractTransactions" />
        </div>
      </div>
    </div>
    <div class="flex flex-col px-2 py-2 w-full bg-slate-100 dark:dark:bg-zinc-700" v-else>
      <div class="text-sm">
        Please select an intelligent contract first, you can go to
        <RouterLink :to="{ name: 'simulator.contracts' }" class="text-primary">
          Files llist.
        </RouterLink>
      </div>
    </div>
  </div>
</template>
