<script setup lang="ts">
import { HomeIcon, XMarkIcon, DocumentCheckIcon } from '@heroicons/vue/24/solid'
import CodeEditor from '@/components/Simulator/CodeEditor.vue'
import { useContractsFilesStore } from '@/stores';
import { computed, ref } from 'vue';
import Modal from '@/components/ModalComponent.vue'
import HomeTab from './HomeTab.vue'
import { notify } from '@kyvg/vue3-notification';
import { rpcClient } from '@/utils';


const store = useContractsFilesStore()

const defaultStateModalOpen = ref(false)
const defaultContractState = ref('{}')
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

const handleDeployContractRequest = (id: string) => {
    if (store.currentContractId === id) {
        defaultStateModalOpen.value = true
    }
}

const closeDefaultStateModal = () => {
    defaultStateModalOpen.value = false
}

const setCurrentContractTab = (id?: string) => {
    store.currentContractId = id
}
const handleCloseContract = (id?: string) => {
    store.closeFile(id || '')
}
const contracts = computed(() => {
    return store.contracts.filter(contract => store.openedFiles.includes(contract.id || ''))
})

</script>

<template>
    <div class="flex flex-col w-full h-full">
        <nav class="border-b text-sm flex justify-start items-center">
            <div class="font-semibold flex justify-between px-2 py-2 text-neutral-500 hover:border-primary hover:text-primary"
                :class="{ 'border-b-2 border-primary text-primary': !store.currentContractId }">
                <button class="bg-transparent mr-2 flex" @click="setCurrentContractTab()">
                    <HomeIcon class="mx-2 h-4 w-4" :class="{ 'fill-primary': !store.currentContractId }" />
                </button>
            </div>
            <div v-for="contract in contracts" :key="contract.id"
                class="font-semibold flex justify-between px-2 py-2 text-neutral-500 hover:border-primary hover:text-primary"
                :class="{ 'border-b-2 border-primary text-primary': contract.id === store.currentContractId }">
                <button class="bg-transparent flex" @click="setCurrentContractTab(contract.id)">
                    <DocumentCheckIcon class="h-4 w-4 mr-2"
                        :class="{ 'fill-primary': contract.id === store.currentContractId }" />
                    {{ contract.name }}.genpy
                </button>
                <button class="bg-transparent" @click="handleCloseContract(contract.id)">
                    <XMarkIcon class="ml-4 h-4 w-4" />
                </button>

            </div>
        </nav>
        <div v-show="!store.currentContractId" class="flex w-full h-full">
            <HomeTab v-show="!store.currentContractId" />
        </div>
        <div v-for="contract in contracts" :key="contract.id" class="flex w-full h-full relative"
            v-show="contract.id === store.currentContractId">
            <CodeEditor :contract="contract" @deploy="handleDeployContractRequest" />
        </div>

        <Modal :open="defaultStateModalOpen" @close="closeDefaultStateModal">
            <div class="flex flex-col">
                <div class="flex flex-col">
                    <h2>Set the default contrat state</h2>
                    <p>Please provide a json object with the default contract state.</p>
                </div>
                <div class="flex mt-2">
                    <textarea rows="10" class="w-full bg-slate-100 dark:dark:bg-zinc-700 p-2"
                        v-model="defaultContractState" clear-icon="ri-close-circle" label="State" />
                </div>
                <div class="flex justify-end mt-4">
                    <button class="bg-primary text-white px-4 py-2 rounded" @click="handleDeployContract">
                        Deploy contract
                    </button>
                </div>
            </div>
        </Modal>
    </div>
</template>
