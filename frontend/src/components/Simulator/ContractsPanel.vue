<script setup lang="ts">
import { HomeIcon, XMarkIcon, DocumentCheckIcon } from '@heroicons/vue/24/solid'
import CodeEditor from '@/components/Simulator/CodeEditor.vue'
import { useContractsFilesStore } from '@/stores';
import { computed } from 'vue';
import HomeTab from './HomeTab.vue'
import { useRouter } from 'vue-router';



const store = useContractsFilesStore()
const router = useRouter()
const handleRunDebug = () => {
    router.push({ name: 'simulator.run-debug' })
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
                    {{ contract.name }}.gpy
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
            <CodeEditor :contract="contract" @run-debug="handleRunDebug" />
        </div>
    </div>
</template>
