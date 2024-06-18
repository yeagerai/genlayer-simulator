<script setup lang="ts">
import { useAccountsStore, useContractsStore } from '@/stores'
import { computed, onMounted, watch } from 'vue'
import { notify } from '@kyvg/vue3-notification'
import ContractState from '@/components/Simulator/ContractState.vue'
import ExecuteTransactions from '@/components/Simulator/ExecuteTransactions.vue'
import TransactionsList from '@/components/Simulator/TransactionsList.vue'
import ConstructorParameters from '@/components/Simulator/ConstructorParameters.vue'
import { debounce } from 'vue-debounce'


const store = useContractsStore()
const accounts = useAccountsStore()

const contractTransactions = computed(() => {
  if (store.deployedContract?.address && store.transactions[store.deployedContract?.address]) {
    return store.transactions[store.deployedContract?.address]
  }
  return []
})

const handleGetContractState = async (
  contractAddress: string,
  method: string,
  methodArguments: string[]
) => {
  try {
    await store.getContractState(contractAddress, method, methodArguments)
  } catch (error) {
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error getting contract state',
      type: 'error'
    })
  }
}

const handleCallContractMethod = async ({ method, params }: { method: string; params: any[] }) => {
  const result = await store.callContractMethod({
    userAccount: accounts.currentUserAddress || '',
    contractAddress: store.deployedContract?.address || '',
    method: `${store.currentDeployedContractAbi?.class}.${method}`,
    params
  })
  if (!result) {
    notify({
      title: 'Error',
      text: 'Error calling contract method',
      type: 'error'
    })
  }
}

const handleDeployContract = async ({
  params: constructorParams
}: {
  params: { [k: string]: string }
}) => {
  try {
    await store.deployContract({
      constructorParams
    })
    notify({
      title: 'OK',
      text: 'Contract deployed',
      type: 'success'
    })
  } catch (err) {
    notify({
      title: 'Error',
      text: (err as Error)?.message || 'Error deploying contract',
      type: 'error'
    })
  }
}


const debouncedGetConstructorInputs = debounce(() => store.getConstructorInputs(), 3000)

watch(() => store.deployedContract?.contractId, (newValue) => {
  if (newValue) {
    store.getCurrentContractAbi()
  }
})


watch(() => store.currentContract?.id, (newValue, oldValue) => {
  if (newValue && newValue !== oldValue) {
    store.getConstructorInputs()
  }
})

watch(() => store.currentContract?.content, (newValue, oldValue) => {
  if (newValue && newValue !== oldValue && !store.loadingConstructorInputs) {
    debouncedGetConstructorInputs()
  }
})
watch(() => store.currentErrorConstructorInputs, (newValue, oldValue) => {
  if (newValue && newValue !== oldValue) {
    notify({
      title: 'Error',
      text: 'Error getting the contract schema',
      type: 'error'
    })
  }
})

onMounted(async () => {
  await store.getConstructorInputs()
  if (store.deployedContract) {
    store.getCurrentContractAbi()
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
            {{ store.currentContract?.name }}
          </div>
        </div>
        <ConstructorParameters :inputs="store.currentConstructorInputs" :loading="store.loadingConstructorInputs"
          :error="store.currentErrorConstructorInputs" @deploy-contract="handleDeployContract"
          :deploying="store.deployingContract" />
      </div>
      <div class="flex flex-col" v-show="store.deployedContract">
        <div class="flex flex-col">
          <ContractState :abi="store.currentDeployedContractAbi" :contract-state="store.currentContractState"
            :deployed-contract="store.deployedContract" :get-contract-state="handleGetContractState"
            :calling-state="store.callingContractState" />
        </div>

        <div class="flex flex-col">
          <ExecuteTransactions :abi="store.currentDeployedContractAbi" @call-method="handleCallContractMethod"
            :calling-method="store.callingContractMethod" />
        </div>
        <div class="flex flex-col">
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
