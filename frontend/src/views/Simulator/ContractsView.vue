<script setup lang="ts">
import { useContractsStore } from '@/stores'
import { ArrowUpTrayIcon, PlusIcon } from '@heroicons/vue/20/solid'
import { nextTick, ref, watchEffect } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import ContractItem from '@/components/Simulator/ContractItem.vue'

const store = useContractsStore()
const newFileName = ref('.gpy')
const showNewFileInput = ref(false)
const newFileNameInputRef = ref<HTMLInputElement | null>(null)
/**
 * Loads content from a file and adds it to the contract file store.
 *
 * @param {Event} event - The event triggered by the file input element.
 */
const loadContentFromFile = (event: Event) => {
  const target = event.target as HTMLInputElement

  if (target.files && target.files.length > 0) {
    const [file] = target.files
    const reader = new FileReader()

    reader.onload = (ev: ProgressEvent<FileReader>) => {
      if (ev.target?.result) {
        const id = uuidv4()
        store.addContractFile({ id, name: file.name, content: (ev.target?.result as string) || '' })
        store.openFile(id)
      }
    }

    reader.readAsText(file)
  }
}

const handleAddNewFile = () => {
  if (!showNewFileInput.value) {
    showNewFileInput.value = true
  }
}

watchEffect(() => {
  if (showNewFileInput.value && newFileNameInputRef.value) {
    nextTick(() => {
      newFileNameInputRef?.value?.focus()
      newFileNameInputRef?.value?.setSelectionRange(0, 0)
    })
  }
})

const handleSaveNewFile = () => {
  if (newFileName.value && newFileName.value.replace('.gpy', '') !== '') {
    const id = uuidv4()
    store.addContractFile({ id, name: newFileName.value, content: '' })
    store.openFile(id)
  }

  showNewFileInput.value = false
  newFileName.value = '.gpy'
}
</script>
<template>
  <div class="flex w-full flex-col">
    <div class="flex w-full flex-row items-start justify-between gap-2 p-2">
      <h3 class="text-xl">Your Contracts</h3>
      <div class="flex flex-row items-center gap-2">
        <GhostBtn @click="handleAddNewFile">
          <PlusIcon class="h-5 w-5" />
          <ToolTip text="New Contract" :options="{ placement: 'bottom' }" />
        </GhostBtn>

        <GhostBtn class="!p-0">
          <label class="input-label p-1">
            <input type="file" @change="loadContentFromFile" accept=".gpy,.py" />
            <ArrowUpTrayIcon class="h-5 w-5 fill-primary dark:fill-white" />
            <ToolTip text="Add From File" :options="{ placement: 'bottom' }" />
          </label>
        </GhostBtn>
      </div>
    </div>

    <ContractItem
     @click="store.openFile(contract.id)"
      v-for="contract in store.contracts"
      :key="contract.id"
      :contract="contract"
      :isActive="contract.id === store.currentContractId"
    />

    <div
      class="flex w-full flex-col items-center justify-between border border-transparent px-2 py-1 font-semibold text-neutral-500"
      v-show="showNewFileInput"
    >
      <input
        type="text"
        ref="newFileNameInputRef"
        class="w-full bg-slate-100 dark:dark:bg-zinc-700"
        v-model="newFileName"
        @blur="handleSaveNewFile"
        @keyup.enter="handleSaveNewFile"
        @keydown.escape="handleSaveNewFile"
      />
    </div>
  </div>
</template>

<style scoped>
.input-label {
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.input-label input {
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  opacity: 0;
}
</style>
