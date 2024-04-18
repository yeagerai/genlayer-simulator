<script setup lang="ts">
import { useContractsFilesStore } from "@/stores"
import { computed, ref } from "vue";
import { rpcClient } from '@/utils';
import { notify } from "@kyvg/vue3-notification";


const store = useContractsFilesStore()

const defaultStateModalOpen = ref(false)
const defaultContractState = ref('{}')

const contract = computed(() => store.contracts.find(contract => contract.id === store.currentContractId))

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
      defaultStateModalOpen.value = false

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

</script>

<template>
  <div class="flex flex-col w-full">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Run and Debug</h3>
    </div>
    <div class="flex flex-col px-2 py-2 w-full bg-slate-100">
      <div>Intelligent Contract:</div>
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
        <textarea rows="10" class="w-full bg-slate-100 dark:dark:bg-zinc-700 p-2" v-model="defaultContractState"
          clear-icon="ri-close-circle" label="State" />
      </div>
    </div>
    <div class="flex flex-col p-2 w-full justify-center">
      <ToolTip text="Deploy" :options="{ placement: 'top' }" />
      <button @click="handleDeployContract"
        class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">Deploy Intelligent
        Contract</button>
    </div>
  </div>
</template>
