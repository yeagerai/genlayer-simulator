<script setup lang="ts">
import { useNodeStore } from '@/stores'
import { type ValidatorModel } from '@/types'
import { notify } from '@kyvg/vue3-notification'

const nodeStore = useNodeStore()

const props = defineProps<{
  validator: ValidatorModel
}>()
const emit = defineEmits(['close'])

async function handleDeleteValidator() {
  try {
    await nodeStore.deleteValidator(props.validator)
    notify({
      title: 'OK',
      text: 'Validator deleted successfully',
      type: 'success',
    })
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error deleting a validator',
      type: 'error',
    })
  } finally {
    emit('close')
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
    <div class="mt-2 flex flex-col p-2">
      <p class="text-md font-semibold">Address:</p>

      <div class="w-full py-2">
        {{ validator.address }}
      </div>
    </div>
    <div class="mt-2 flex flex-col p-2">
      <p class="text-md font-semibold">Provider:</p>
      {{ validator.provider }}
    </div>
    <div class="mt-2 flex flex-col p-2">
      <p class="text-md font-semibold">Model:</p>
      {{ validator.model }}
    </div>
    <div class="mt-2 flex flex-col p-2">
      <p class="text-md font-semibold">Stake:</p>
      {{ validator.stake }}
    </div>
  </ConfirmationModal>
</template>
