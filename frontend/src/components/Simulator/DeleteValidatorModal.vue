<script setup lang="ts">
import { useNodeStore } from '@/stores';
import { type ValidatorModel } from '@/types';
import { notify } from '@kyvg/vue3-notification';
import FieldLabel from '@/components/global/fields/FieldLabel.vue';

const nodeStore = useNodeStore();

const props = defineProps<{
  validator: ValidatorModel;
}>();
const emit = defineEmits(['close']);

async function handleDeleteValidator() {
  try {
    await nodeStore.deleteValidator(props.validator);
    notify({
      title: 'Validator deleted',
      type: 'success',
    });
  } catch (error) {
    console.error(error);
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error deleting a validator',
      type: 'error',
    });
  } finally {
    emit('close');
  }
}
</script>

<template>
  <ConfirmationModal
    @close="emit('close')"
    @confirm="handleDeleteValidator"
    :buttonText="`Delete Validator #${validator.id}`"
    buttonTestId="btn-delete-validator"
    dangerous
  >
    <template #title>Delete Validator</template>

    <div>
      <FieldLabel>Address</FieldLabel>
      <div class="text-xs">
        {{ validator.address }}
      </div>
    </div>

    <div>
      <FieldLabel>Provider</FieldLabel>
      <div class="text-xs">
        {{ validator.provider }}
      </div>
    </div>

    <div>
      <FieldLabel>Model</FieldLabel>
      <div class="text-xs">
        {{ validator.model }}
      </div>
    </div>

    <div>
      <FieldLabel>Stake</FieldLabel>
      <div class="text-xs">
        {{ validator.stake }}
      </div>
    </div>
  </ConfirmationModal>
</template>
