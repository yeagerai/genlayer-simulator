<script setup lang="ts">
import { HomeIcon, PlayIcon } from '@heroicons/vue/24/solid'
import ContractTab from '@/components/Simulator/ContractTab.vue'
import CodeEditor from '@/components/Simulator/CodeEditor.vue'
import { useContractsStore } from '@/stores';
import { computed } from 'vue';
import HomeTab from './HomeTab.vue'
import { useRouter } from 'vue-router';

const store = useContractsStore()
const router = useRouter()

const handleRunDebug = () => {
    router.push({ name: 'simulator.run-debug' })
}

const setCurrentContractTab = (id?: string) => {
    console.log(' setCurrentContractTab', id)
    store.setCurrentContractId(id)
}

const handleCloseContract = (id?: string) => {
    store.closeFile(id || '')
}

const contracts = computed(() => {
    return store.contracts.filter(contract => store.openedFiles.includes(contract.id || ''))
})

const showHome = computed(() => store.currentContractId === '')
</script>

<template>
    <div class="flex flex-col w-full h-full">
        <nav class="border-b text-sm flex justify-between items-center">
            <div class="flex justify-start items-center">
                <div id="tutorial-welcome"
                    class="font-semibold flex justify-between px-2 py-2 text-neutral-500  hover:border-primary hover: dark:text-white"
                    :class="{ 'border-b-2 border-primary  dark:text-white text-primary': showHome }">
                    <button class="bg-transparent mr-2 flex" @click="setCurrentContractTab('')">
                        <HomeIcon class="mx-2 h-4 w-4" :class="{ 'dark:fill-white fill-primary': showHome }" />
                    </button>
                </div>

                <ContractTab v-for="contract in contracts" :key="contract.id" :contract="contract"
                    :isActive="contract.id === store.currentContractId"
                    @closeContract="handleCloseContract(contract.id)"
                    @selectContract="setCurrentContractTab(contract.id)" />
            </div>
            <div class="flex p-2 mr-3">
                <button class="flex ml-3" @click="handleRunDebug">
                    <PlayIcon class="h-5 w-5 dark:fill-white fill-primary" />
                    <ToolTip text="Run and Debug" :options="{ placement: 'bottom' }" />
                </button>
            </div>
        </nav>
        <div v-show="showHome" class="flex w-full h-full">
            <HomeTab />
        </div>
        <div v-for="contract in contracts" :key="contract.id" class="flex w-full h-full relative"
            v-show="contract.id === store.currentContractId">
            <CodeEditor :contract="contract" @run-debug="handleRunDebug" />
        </div>
    </div>
</template>
