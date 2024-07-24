<script setup lang="ts">
const emit = defineEmits(['confirm', 'close'])

const props = withDefaults(
  defineProps<{
    buttonText?: string
    buttonTestId?: string
    dangerous?: boolean
    confirming?: boolean
  }>(),
  {
    buttonText: 'Confirm',
    buttonTestId: 'confirm-button',
    dangerous: false,
    confirming: false,
  },
)
</script>

<template>
  <Modal @close="emit('close')">
    <template #title v-if="!$slots.title">Are you sure?</template>
    <template #title v-else><slot name="title" /></template>

    <template #description><slot name="description" /></template>

    <slot />

    <div class="flex flex-row gap-4">
      <Btn secondary @click="emit('close')" class="flex-1">Cancel</Btn>
      <Btn
        :dangerous="dangerous"
        @click="emit('confirm')"
        :id="buttonTestId"
        :loading="confirming"
        class="flex-auto"
        >{{ buttonText }}</Btn
      >
    </div>
  </Modal>
</template>
