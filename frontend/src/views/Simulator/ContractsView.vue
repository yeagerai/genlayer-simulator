<script setup lang="ts">
import { useContractsFilesStore } from "@/stores"
import { DocumentCheckIcon, ArrowUpTrayIcon, PlusIcon, TrashIcon, PencilIcon } from '@heroicons/vue/24/solid'
import { ref } from "vue";
import { v4 as uuidv4 } from 'uuid'
const store = useContractsFilesStore()
const showFileOptionsId = ref('')
const editingFileId = ref('')
const editingFileName = ref('')
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

}

const handleSaveNewFile = () => {
  // store new empty file
  // open new tab
}

const handleRemoveFile = (id?: string) => {
  store.removeContractFile(id || '')
  if (store.currentContractId === id) {
    store.setCurrentContractId('')
  }
}

const handleEditFile = ({ id, name }: { id: string, name: string }) => {
  editingFileId.value = id
  editingFileName.value = name
}

const handleSaveFile = (e: Event) => {
  e.preventDefault()
  store.updateContractFile(editingFileId.value, { name: editingFileName.value })
  editingFileId.value = ""
  editingFileName.value = ""
}

const showFileOptions = (id?: string) => {
  showFileOptionsId.value = id || ''
}

const openContract = (id?: string) => {
  store.openFile(id || '')
}
</script>
<template>
  <div class="flex flex-col w-full">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Your Contracts</h3>
    </div>
    <div class="flex px-1 py-2 w-full">
      <button class="flex ml-3" @click="handleAddNewFile">
        <PlusIcon class="h-5 w-5 fill-primary" />
        <ToolTip text="Add New Contract" :options="{ placement: 'bottom' }" />
      </button>
      <label class="input-label ml-3">
        <div class="flex">
          <ArrowUpTrayIcon class="h-5 w-5 fill-primary" />
          <ToolTip text="Upload File" :options="{ placement: 'bottom' }" />
          <input type="file" @change="loadContentFromFile" accept=".gpy,.py">
        </div>
      </label>
    </div>
    <div v-for="(contract, index) in store.contracts" :key="contract.id" class="flex flex-col w-full">
      <div @mouseover="showFileOptions(contract.id)" @mouseout="showFileOptions()"
        :class="[index > 0 ? 'border-x border-b' : 'border', 'flex items-center text-xs text-neutral-500 py-1 px-2 font-semibold hover:border-green-500', (contract.id === store.currentContractId ? 'border-green-500' : '')]">
        <DocumentCheckIcon class="h-4 w-4 fill-primary mr-1" />

        <div class="flex items-center justify-between w-full" v-if="editingFileId === contract.id">
          <input type="text" class="bg-slate-100 dark:dark:bg-zinc-700 w-full" v-model="editingFileName"
            @blur="handleSaveFile" @keyup.enter="handleSaveFile">
        </div>
        <div class="flex items-center justify-between w-full" v-else>
          <div class="flex max-w-[80%] cursor-pointer" @click="openContract(contract.id)">
            {{ contract.name }}
          </div>
          <div class="flex" v-show="showFileOptionsId === contract.id">
            <button @click="handleEditFile({ id: contract.id, name: contract.name })">
              <ToolTip text="Edit Name" :options="{ placement: 'bottom' }" />
              <PencilIcon class="h-3 w-4 mr-1" />
            </button>
            <button @click="handleRemoveFile(contract.id)">
              <ToolTip text="Delete file" :options="{ placement: 'bottom' }" />
              <TrashIcon class="h-4 w-4 mr-1" />
            </button>
          </div>
        </div>

      </div>
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