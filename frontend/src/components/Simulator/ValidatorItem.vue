<script setup lang="ts">
import { type ValidatorModel } from '@/types'
import { PencilSquareIcon, TrashIcon } from '@heroicons/vue/24/solid'
import UpdateValidatorModal from '@/components/Simulator/UpdateValidatorModal.vue'
import DeleteValidatorModal from '@/components/Simulator/DeleteValidatorModal.vue'
import { ref } from 'vue'

const isUpdateModalMopen = ref(false)
const isDeleteModalOpen = ref(false)

const props = defineProps<{
  validator: ValidatorModel
}>()
</script>

<template>
  <div
    data-testid="validator-item-container"
    class="group flex cursor-pointer items-center justify-between p-1 px-2 hover:bg-slate-100 dark:hover:bg-zinc-700"
    @click="isUpdateModalMopen = true"
  >
    <div class="flex items-center" data-testid="validator-item">
      <div class="flex text-primary dark:text-white">{{ validator.id }} -</div>
      <div class="ml-2 flex flex-col items-start">
        <div class="flex">
          <span class="mr-1 font-semibold">Model: </span>
          <span class="text-primary dark:text-white" data-testid="validator-item-model">{{
            validator.model
          }}</span>
        </div>
        <div class="flex">
          <span class="mr-1 font-semibold">Provider: </span>
          <span data-testid="validator-item-provider">{{ validator.provider }}</span>
        </div>
      </div>
    </div>

    <div class="hidden flex-row gap-1 group-hover:flex">
      <button @click.stop="isUpdateModalMopen = true">
        <PencilSquareIcon
          class="h-[16px] w-[16px] p-[2px] text-gray-400 transition-all hover:text-gray-800 active:scale-90 dark:hover:text-white"
        />
        <ToolTip text="Update Validator" :options="{ placement: 'bottom' }" />
      </button>

      <button @click.stop="isDeleteModalOpen = true">
        <TrashIcon
          class="h-[16px] w-[16px] p-[2px] text-gray-400 transition-all hover:text-gray-800 active:scale-90 dark:hover:text-white"
        />
        <ToolTip text="Delete validator" :options="{ placement: 'bottom' }" />
      </button>
    </div>
  </div>

  <UpdateValidatorModal
    :validator="validator"
    :open="isUpdateModalMopen"
    @close="isUpdateModalMopen = false"
  />

  <DeleteValidatorModal
    :validator="validator"
    :open="isDeleteModalOpen"
    @close="isDeleteModalOpen = false"
  />
</template>
