<script setup lang="ts">
import { useContractsStore } from '@/stores'
import { type ContractFile } from '@/types'
import { DocumentCheckIcon, PencilSquareIcon, TrashIcon } from '@heroicons/vue/16/solid'
import { nextTick } from 'process'
import { ref } from 'vue'

const store = useContractsStore()

const props = defineProps<{
  contract: ContractFile
  isActive: Boolean
}>()

const isEditing = ref(false)
const editInput = ref<HTMLInputElement | null>(null)
const editingFileName = ref('')
const deleteModalOpen = ref(false)

const handleEditFile = ({ id, name }: { id: string; name: string }) => {
  isEditing.value = true
  editingFileName.value = name
  const dotPosition = name.indexOf('.')

  nextTick(() => {
    editInput.value?.focus()
    editInput.value?.setSelectionRange(0, dotPosition)
  })
}

const handleStopEditing = () => {
  isEditing.value = false
  editingFileName.value = ''
  editInput.value?.blur()
}

const handleSaveFile = (e: Event) => {
  e.preventDefault()

  if (isEditing.value === false) {
    return // Avoid double events with enter + blur
  }

  store.updateContractFile(props.contract.id, { name: editingFileName.value })
  isEditing.value = false
  editingFileName.value = ''
  editInput.value?.blur()
}

const handleRemoveFile = () => {
  store.removeContractFile(props.contract.id)
  deleteModalOpen.value = false
}
</script>

<template>
  <div class="flex w-full cursor-pointer flex-col">
    <div
      :class="[
        'group flex items-center px-2 py-1.5 text-xs transition-colors hover:bg-gray-50',
        isActive &&
          'bg-gray-200 hover:bg-gray-200 dark:bg-zinc-600 dark:text-white hover:dark:bg-zinc-600',
        !isActive &&
          'bg-white text-neutral-500 hover:bg-gray-100 dark:bg-zinc-800 hover:dark:bg-zinc-700',
      ]"
    >
      <DocumentCheckIcon class="mr-1 h-4 w-4 fill-primary dark:fill-white" />

      <div class="flex w-full items-center justify-between" v-if="isEditing">
        <input
          type="text"
          ref="editInput"
          class="w-full bg-slate-100 dark:bg-zinc-700"
          v-model="editingFileName"
          @blur="handleSaveFile"
          @keydown.enter="handleSaveFile"
          @keydown.escape="handleStopEditing"
        />
      </div>

      <div v-else class="flex w-full items-center justify-between truncate">
        <div class="... truncate font-semibold">
          {{ contract.name }}
        </div>

        <div class="hidden flex-row gap-1 group-hover:flex">
          <button @click="handleEditFile({ id: contract.id, name: contract.name })">
            <PencilSquareIcon
              class="h-3 w-3 text-gray-400 transition-all hover:text-gray-800 active:scale-90 dark:hover:text-white"
            />
            <ToolTip text="Edit Name" :options="{ placement: 'bottom' }" />
          </button>

          <button @click="deleteModalOpen = true">
            <TrashIcon
              class="h-3 w-3 text-gray-400 transition-all hover:text-gray-800 active:scale-90 dark:hover:text-white"
            />
            <ToolTip text="Delete file" :options="{ placement: 'bottom' }" />
          </button>
        </div>
      </div>

      <ConfirmationModal
        :open="deleteModalOpen"
        @close="deleteModalOpen = false"
        @confirm="handleRemoveFile"
        buttonText="Delete Contract"
        dangerous
      >
        <template #title>Delete Contract</template>
        <template #description>Are you sure you want to delete this contract?</template>
        <template #info>{{ contract.name }}</template>
      </ConfirmationModal>
    </div>
  </div>
</template>
