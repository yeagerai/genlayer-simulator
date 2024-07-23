<script setup lang="ts">
import { useContractsStore } from '@/stores'
import {
  DocumentCheckIcon,
  ArrowUpTrayIcon,
  PlusIcon,
  TrashIcon,
  PencilIcon,
} from '@heroicons/vue/24/solid'
import { nextTick, ref, watchEffect } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import type { ContractFile } from '@/types'

const store = useContractsStore()
const editingFileId = ref('')
const newFileName = ref('.gpy')
const showNewFileInput = ref(false)
const editingFileName = ref('')
const newFileNameInputRef = ref<HTMLInputElement | null>(null)
const deleteFileModalIsOpen = ref(false)
const fileToDelete = ref<ContractFile | null>(null)
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
        store.addContractFile({
          id,
          name: file.name,
          content: (ev.target?.result as string) || '',
        })
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

const handleRemoveFile = () => {
  if (fileToDelete.value) {
    store.removeContractFile(fileToDelete.value.id)
    if (store.currentContractId === fileToDelete.value.id) {
      store.setCurrentContractId('')
    }
  }

  deleteFileModalIsOpen.value = false
}

const handleEditFile = ({ id, name }: { id: string; name: string }) => {
  editingFileId.value = id
  editingFileName.value = name
}

const handleSaveFile = (e: Event) => {
  e.preventDefault()
  store.updateContractFile(editingFileId.value, { name: editingFileName.value })
  editingFileId.value = ''
  editingFileName.value = ''
}

const openContract = (id?: string) => {
  store.openFile(id || '')
}

const openDeleteFileModal = (contract: ContractFile) => {
  fileToDelete.value = contract
  deleteFileModalIsOpen.value = true
}

const closeDeleteFileModal = () => {
  deleteFileModalIsOpen.value = false
  fileToDelete.value = null
}
</script>
<template>
  <div class="flex w-full flex-col">
    <div class="flex w-full flex-col p-2">
      <h3 class="text-xl">Your Contracts</h3>
    </div>
    <div class="flex w-full px-1 py-2">
      <button class="ml-3 flex" @click="handleAddNewFile">
        <PlusIcon class="h-5 w-5 fill-primary dark:fill-white" />
        <ToolTip text="Add New Contract" :options="{ placement: 'bottom' }" />
      </button>
      <label class="input-label ml-3">
        <div class="flex">
          <ArrowUpTrayIcon class="h-5 w-5 fill-primary dark:fill-white" />
          <ToolTip text="Upload File" :options="{ placement: 'bottom' }" />
          <input type="file" @change="loadContentFromFile" accept=".gpy,.py" />
        </div>
      </label>
    </div>
    <div
      v-for="contract in store.contracts"
      :key="contract.id"
      class="flex w-full flex-col"
    >
      <div
        :class="[
          'group flex items-center px-2 py-1 text-xs font-semibold text-neutral-500 hover:text-primary hover:underline dark:text-neutral-100',
          contract.id === store.currentContractId
            ? 'text-primary underline'
            : '',
        ]"
      >
        <DocumentCheckIcon class="mr-1 h-4 w-4 fill-primary dark:fill-white" />

        <div
          class="flex w-full items-center justify-between"
          v-if="editingFileId === contract.id"
        >
          <input
            type="text"
            class="w-full bg-slate-100 dark:bg-zinc-700"
            v-model="editingFileName"
            @blur="handleSaveFile"
            @keyup.enter="handleSaveFile"
          />
        </div>
        <div v-else class="flex w-full items-center justify-between truncate">
          <div
            class="... cursor-pointer truncate"
            @click="openContract(contract.id)"
          >
            {{ contract.name }}
          </div>
          <div class="hidden group-hover:flex">
            <button
              @click="handleEditFile({ id: contract.id, name: contract.name })"
            >
              <ToolTip text="Edit Name" :options="{ placement: 'bottom' }" />
              <PencilIcon class="mr-1 h-3 w-4" />
            </button>
            <button @click="openDeleteFileModal(contract)">
              <ToolTip text="Delete file" :options="{ placement: 'bottom' }" />
              <TrashIcon class="mr-1 h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
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
  <Modal :open="deleteFileModalIsOpen" @close="closeDeleteFileModal">
    <div class="flex flex-col">
      <div class="flex justify-between">
        <div class="text-xl">Delete Contract</div>
      </div>
      <div class="mt-4 flex justify-between p-2">
        Are you sure you want to delete this contract?
      </div>
      <div class="flex flex-col p-2">
        <div class="w-full bg-slate-100 py-2 text-center font-bold">
          {{ fileToDelete?.name }}
        </div>
      </div>
    </div>
    <div class="mt-4 flex w-full flex-col">
      <Btn @click="handleRemoveFile">Delete</Btn>
    </div>
  </Modal>
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
