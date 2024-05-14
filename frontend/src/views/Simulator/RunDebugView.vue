<script setup lang="ts">
import { useMainStore } from '@/stores'
import { computed, onMounted, ref, watch, inject } from 'vue'
import { notify } from '@kyvg/vue3-notification'
import ContractState from '@/components/Simulator/ContractState.vue'
import ExecuteTransactions from '@/components/Simulator/ExecuteTransactions.vue'
import TransactionsList from '@/components/Simulator/TransactionsList.vue'
import ConstructorParameters from '@/components/Simulator/ConstructorParameters.vue'
import type { DeployedContract } from '@/types'
import type { IJsonRPCService } from '@/services'

const store = useMainStore()
const $jsonRpc = inject<IJsonRPCService>('$jsonRpc')!
const constructorInputs = ref<{ [k: string]: string }>({})
const abi = ref<any>()
const contractState = ref<any>({})
const contract = computed(() =>
  store.contracts.find((contract) => contract.id === store.currentContractId)
)
const deployedContract = computed(() =>
  store.deployedContracts.find((contract) => contract.contractId === store.currentContractId)
)
const contractTransactions = ref<any[]>([])

const handleGetContractState = async (
  contractAddress: string,
  method: string,
  methodArguments: string[]
) => {
  const { result } = await $jsonRpc.call({
    method: 'get_contract_state',
    params: [contractAddress, method, methodArguments]
  })

  contractState.value = {
    ...contractState.value,
    [method]: result.data[method]
  }
}

const handleCallContractMethod = async ({ method, params }: { method: string; params: any[] }) => {
  console.log('handleCallContractMethod', method, params, abi.value.class)
  const { result } = await $jsonRpc.call({
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

const handleDeployContract = async ({
  params: constructorParams
}: {
  params: { [k: string]: string }
}) => {
  const contract = store.contracts.find((c) => c.id === store.currentContractId)
  if (contract) {
    if (
      Object.keys({ ...constructorInputs.value }).length !== Object.keys(constructorParams).length
    ) {
      notify({
        title: 'Error',
        text: 'You should provide a valid default state',
        type: 'error'
      })
    } else {
      // Getting the ABI to check the class name
      const {
        result: { data: contractSchema }
      } = await $jsonRpc.call({
        method: 'get_icontract_schema_for_code',
        params: [contract.content]
      })

      // Deploy the contract
      const constructorParamsAsString = JSON.stringify(constructorParams)
      const { result } = await $jsonRpc.call({
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
          text:
            typeof result.message === 'string' ? result.message : 'Error Deploying the contract',
          type: 'error'
        })
      }
    }
  }
}

const setDefaultState = async (contract: DeployedContract) => {
  try {
    // constructorInputs.value = JSON.parse(contract.defaultState || '{}')
    // TODO: check if we need to update again also we have an issue with conversion
    // between `bool` in Python with value `True` vs JSON boolean with value `true`

    const { result } = await $jsonRpc.call({
      method: 'get_icontract_schema',
      params: [contract.address]
    })

    abi.value = result.data
  } catch (error) {
    console.error(error)
    store.removeDeployedContract(contract.contractId)
  }
}

const getConstructorInputs = async () => {
  if (contract.value) {
    const { result } = await $jsonRpc.call({
      method: 'get_icontract_schema_for_code',
      params: [contract.value.content]
    })
    constructorInputs.value = result.data?.methods['__init__']?.inputs
  }
}

watch(deployedContract, (newValue) => {
  if (newValue) {
    setDefaultState(newValue)
  }
})

watch(contract, (newValue) => {
  if (newValue) {
    getConstructorInputs()
  }
})

onMounted(() => {
  getConstructorInputs()

  if (deployedContract.value) {
    setDefaultState(deployedContract.value)
  }
})
</script>

<template>
  <div class="flex flex-col w-full overflow-y-auto max-h-[93vh]">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Run and Debug</h3>
    </div>
    <div class="flex flex-col overflow-y-auto" v-if="!!store.currentContractId">
      <div class="flex flex-col">
        <div class="flex flex-col px-2 py-2 w-full bg-slate-100 dark:bg-zinc-700">
          <div class="text-sm">Intelligent Contract:</div>
          <div class="text-xs text-neutral-800 dark:text-neutral-200">
            {{ contract?.name }}
          </div>
        </div>
        <ConstructorParameters
          :inputs="constructorInputs"
          @deploy-contract="handleDeployContract"
        />
      </div>
      <div class="flex flex-col" v-show="deployedContract">
        <div class="flex flex-col">
          <ContractState
            :abi="abi"
            :contract-state="contractState"
            :deployed-contract="deployedContract"
            :get-contract-state="handleGetContractState"
          />
        </div>

        <div class="flex flex-col">
          <ExecuteTransactions :abi="abi" @call-method="handleCallContractMethod" />
        </div>
        <div id="tutorial-node-output" class="flex flex-col">
          <TransactionsList :transactions="contractTransactions" />
        </div>
      </div>
    </div>
    <div class="flex flex-col px-2 py-2 w-full bg-slate-100 dark:dark:bg-zinc-700" v-else>
      <div class="text-sm">
        Please select an intelligent contract first, you can go to
        <RouterLink :to="{ name: 'simulator.contracts' }" class="text-primary dark:text-white">
          Files llist.
        </RouterLink>
      </div>
    </div>
  </div>
</template>
