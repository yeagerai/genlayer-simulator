<script setup lang="ts">
import { PlayIcon } from '@heroicons/vue/24/solid'
import ContractTab from '@/components/Simulator/ContractTab.vue'
import CodeEditor from '@/components/Simulator/CodeEditor.vue'
import { useContractsStore } from '@/stores';
import { computed, ref } from 'vue';
import HomeTab from './HomeTab.vue'
import { useRouter } from 'vue-router';

const store = useContractsStore()
const router = useRouter()
const scrollContainer = ref('')

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

const handleHorizontalScroll = (event: Event) => {
    if (!event.shiftKey) {
        event.preventDefault();
        scrollContainer.value.scrollLeft += event.deltaY;
    }
}
</script>

<template>
    <div class="flex flex-col w-full h-full">
        <nav class="border-b text-sm flex justify-between items-stretch">
            <div ref="scrollContainer" class="flex justify-start items-stretch overflow-x-auto no-scrollbar"
                @wheel.stop="handleHorizontalScroll">

                <ContractTab id="tutorial-welcome" :isHomeTab="true" :isActive="showHome"
                    @selectContract="setCurrentContractTab('')" />

                <ContractTab v-for="contract in contracts" :key="contract.id" :contract="contract"
                    :id="`contract-item-${contract.id}`" :isActive="contract.id === store.currentContractId"
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
