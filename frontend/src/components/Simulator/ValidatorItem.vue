<script setup lang="ts">
import { type ValidatorModel } from '@/types';
import { PencilSquareIcon, TrashIcon } from '@heroicons/vue/24/solid';
import ValidatorModal from '@/components/Simulator/ValidatorModal.vue';
import DeleteValidatorModal from '@/components/Simulator/DeleteValidatorModal.vue';
import { ref } from 'vue';

const isUpdateModalMopen = ref(false);
const isDeleteModalOpen = ref(false);

defineProps<{
  validator: ValidatorModel;
}>();
</script>

<template>
  <div
    data-testid="validator-item"
    class="group flex cursor-pointer flex-row items-center justify-between gap-2 bg-slate-100 p-2 hover:bg-slate-200 dark:bg-gray-700 dark:hover:bg-gray-600"
    @click="isUpdateModalMopen = true"
  >
    <div
      class="flex rounded-md bg-slate-400 px-1 py-0.5 text-xs font-semibold text-white dark:bg-gray-200 dark:text-slate-800"
    >
      #{{ validator.id }}
    </div>

    <div class="flex grow flex-col truncate">
      <span
        class="truncate text-xs font-semibold text-gray-500"
        data-testid="validator-item-provider"
      >
        {{ validator.provider }}
      </span>
      <span
        class="truncate text-sm font-semibold"
        data-testid="validator-item-model"
      >
        {{ validator.model }}
      </span>
    </div>

    <div class="invisible flex flex-row gap-1 group-hover:visible">
      <button @click.stop="isUpdateModalMopen = true">
        <PencilSquareIcon
          class="h-5 w-5 p-[2px] text-slate-400 transition-colors hover:text-slate-800 active:scale-90 dark:hover:text-white"
        />
        <ToolTip text="Update Validator" :options="{ placement: 'bottom' }" />
      </button>

      <button
        data-testid="validator-item-delete"
        @click.stop="isDeleteModalOpen = true"
      >
        <TrashIcon
          class="h-5 w-5 p-[2px] text-slate-400 transition-colors hover:text-slate-800 active:scale-90 dark:hover:text-white"
        />
        <ToolTip text="Delete validator" :options="{ placement: 'bottom' }" />
      </button>
    </div>
  </div>

  <ValidatorModal
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
