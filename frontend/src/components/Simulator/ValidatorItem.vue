<script setup lang="ts">
import { type ValidatorModel } from '@/types';
import {
  DocumentDuplicateIcon,
  PencilSquareIcon,
  TrashIcon,
} from '@heroicons/vue/16/solid';
import ValidatorModal from '@/components/Simulator/ValidatorModal.vue';
import DeleteValidatorModal from '@/components/Simulator/DeleteValidatorModal.vue';
import { ref } from 'vue';
import { useNodeStore } from '@/stores';
import { notify } from '@kyvg/vue3-notification';

const nodeStore = useNodeStore();

const isUpdateModalMopen = ref(false);
const isDeleteModalOpen = ref(false);

const props = defineProps<{
  validator: ValidatorModel;
}>();

const handleCloneValidator = () => {
  nodeStore.cloneValidator(props.validator);

  notify({
    title: 'Successfully cloned validator',
    type: 'success',
  });
};
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

    <div class="hidden flex-row gap-1 group-hover:flex">
      <button
        @click.stop="isUpdateModalMopen = true"
        v-tooltip="'Update Validator'"
      >
        <PencilSquareIcon
          class="h-5 w-5 p-[2px] text-slate-400 transition-colors hover:text-slate-800 active:scale-90 dark:hover:text-white"
        />
      </button>

      <button @click.stop="handleCloneValidator" v-tooltip="'Clone Validator'">
        <DocumentDuplicateIcon
          class="h-5 w-5 p-[2px] text-slate-400 transition-colors hover:text-slate-800 active:scale-90 dark:hover:text-white"
        />
      </button>

      <button
        data-testid="validator-item-delete"
        @click.stop="isDeleteModalOpen = true"
        v-tooltip="'Delete Validator'"
      >
        <TrashIcon
          class="h-5 w-5 p-[2px] text-slate-400 transition-colors hover:text-slate-800 active:scale-90 dark:hover:text-white"
        />
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
