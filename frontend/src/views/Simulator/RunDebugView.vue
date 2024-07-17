<script setup lang="ts">
import { useAccountsStore, useContractsStore, useTransactionsStore } from '@/stores'
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { notify } from '@kyvg/vue3-notification'
import ExecuteContractMethods from '@/components/Simulator/ExecuteContractMethods.vue'
import TransactionsList from '@/components/Simulator/TransactionsList.vue'
import ConstructorParameters from '@/components/Simulator/ConstructorParameters.vue'
import { debounce } from 'vue-debounce'


const contractsStore = useContractsStore()
const accountsStore = useAccountsStore()
const transactionsStore = useTransactionsStore()
let deploymentSubscription: () => void
const contractTransactions = computed(() => transactionsStore.transactions.filter((t) => t.localContractId === contractsStore.currentContractId))

const handleGetContractState = async ({ method, params }: { method: string; params: any[] }) => {
  try {
    await contractsStore.getContractState(contractsStore.deployedContract?.address || '', method, params)
  } catch (error) {
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error getting contract state',
      type: 'error'
    })
  }
}

const handleCallContractMethod = async ({ method, params }: { method: string; params: any[] }) => {
  const result = await contractsStore.callContractMethod({
    userAccount: accountsStore.currentUserAddress || '',
    localContractId: contractsStore.deployedContract?.contractId || '',
    method: `${method}`,
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
    await contractsStore.deployContract({
      constructorParams
    })
    notify({
      title: 'OK',
      text: 'Started deploying the contract',
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

const handleClearTransactions = () => {
  transactionsStore.processingQueue = transactionsStore.processingQueue.filter((t) => t.localContractId !== contractsStore.currentContractId)
  transactionsStore.transactions = transactionsStore.transactions.filter((t) => t.localContractId !== contractsStore.currentContractId)
}

const setCurentUserAddress = (event: Event) => {
  if ((event.target as HTMLSelectElement)?.value) {
    accountsStore.currentPrivateKey = (event.target as HTMLSelectElement)?.value as `0x${string}`
  }
}

const debouncedGetConstructorInputs = debounce(() => contractsStore.getConstructorInputs(), 3000)

watch(() => contractsStore.deployedContract?.contractId, (newValue) => {
  if (newValue) {
    contractsStore.getCurrentContractAbi()
  }
})


watch(() => contractsStore.currentContract?.id, (newValue, oldValue) => {
  if (newValue && newValue !== oldValue) {
    contractsStore.getConstructorInputs()
  }
})

watch(() => contractsStore.currentContract?.content, (newValue, oldValue) => {
  if (newValue && newValue !== oldValue && !contractsStore.loadingConstructorInputs) {
    debouncedGetConstructorInputs()
  }
})
watch(() => contractsStore.currentErrorConstructorInputs, (newValue, oldValue) => {
  if (newValue && newValue !== oldValue) {
    notify({
      title: 'Error',
      text: 'Error getting the contract schema',
      type: 'error'
    })
  }
})

onMounted(async () => {
  await contractsStore.getConstructorInputs()
  if (contractsStore.deployedContract) {
    contractsStore.getCurrentContractAbi()
  }
  deploymentSubscription = contractsStore.$onAction(({ name, store, args, after }) => {
    if (name === 'addDeployedContract' && store.$id === contractsStore.$id) {
      after(() => {
        notify({
          title: 'Contract deployed',
          text: `to ${args[0]?.address}`,
          type: 'success'
        })
      })
    }
  })
})

onUnmounted(() => {
  if (deploymentSubscription) {
    deploymentSubscription()
  }
})
</script>

<template>
  <div class="flex flex-col w-full overflow-y-auto max-h-[93vh]">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Run and Debug</h3>
    </div>
    <div class="flex flex-col overflow-y-auto" v-if="!!contractsStore.currentContractId">
      <div class="flex flex-col">
        <div class="flex flex-col px-2 py-2 w-full bg-slate-100 dark:bg-zinc-700">
          <div class="text-sm">Intelligent Contract:</div>
          <div class="text-xs text-neutral-800 dark:text-neutral-200">
            {{ contractsStore.currentContract?.name }}
          </div>
        </div>
        <ConstructorParameters :inputs="contractsStore.currentConstructorInputs"
          :loading="contractsStore.loadingConstructorInputs" :error="contractsStore.currentErrorConstructorInputs"
          @deploy-contract="handleDeployContract" :deploying="contractsStore.deployingContract" />
      </div>
      <div v-if="contractsStore.deployedContract?.address" class="flex flex-col w-full mt-4">
        <div class="flex flex-col justify-start w-full px-4">
          <p>Deployed Contract: </p>
          <span class="text-xs dark:text-white text-primary">{{ contractsStore.deployedContract?.address }}</span>
        </div>
      </div>
      <div class="flex flex-col w-full">
        <div class="flex flex-col px-2 mt-6 py-2 w-full bg-slate-100 dark:bg-zinc-700">
          <h5 class="text-sm">Current Account</h5>
        </div>
        <div class="flex flex-col p-2 my-4 items-start w-full">
          <select name="dropdown-current-account" @change="setCurentUserAddress" class="text-xs w-full dark:bg-zinc-700"
            :value="accountsStore.currentUserAddress">
            <option :value="accountsStore.currentUserAddress">
              {{ accountsStore.currentUserAddress }}
            </option>
            <option v-for="privateKey in accountsStore.privateKeys" :key="privateKey" :value="privateKey">
              {{ accountsStore.accountFromPrivateKey(privateKey).address }}
            </option>
          </select>
        </div>
      </div>

      <div class="flex flex-col" id="tutorial-contract-state">
        <div class="flex flex-col" v-show="contractsStore.deployedContract">
          <ExecuteContractMethods :abi="contractsStore.currentDeployedContractAbi" @call-method="handleGetContractState"
            :calling-method="contractsStore.callingContractState" title="Read Methods" mode="read" 
            :contract-state="contractsStore.currentContractState"/>
        </div>

        <div class="flex flex-col" v-show="contractsStore.deployedContract">
          <ExecuteContractMethods :abi="contractsStore.currentDeployedContractAbi"
            @call-method="handleCallContractMethod" :calling-method="contractsStore.callingContractMethod"
            title="Execute Transactions" mode="write" />
          <div id="tutorial-creating-transactions" class="flex"></div>
        </div>
        <div class="flex flex-col">
          <TransactionsList :transactions="contractTransactions" @clear-transactions="handleClearTransactions" />
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
