<script setup lang="ts">
import { onMounted } from 'vue'
import { notify } from '@kyvg/vue3-notification'
import { useNodeStore } from '@/stores'
import ValidatorItem from '@/components/Simulator/ValidatorItem.vue'
import NewValidatorModal from '@/components/Simulator/NewValidatorModal.vue'
import { ref } from 'vue'

const nodeStore = useNodeStore()
const isNewValidatorModalOpen = ref(false)

// Hooks
onMounted(async () => {
  try {
    await nodeStore.getValidatorsData()
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error loading validators',
      type: 'error',
    })
  }
})

const handleResetStorage = async () => {
  try {
    await nodeStore.resetStorage()
    notify({
      title: 'Success',
      text: 'Storage reset successfully',
      type: 'success',
    })
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error resetting the storage',
      type: 'error',
    })
  } finally {
    nodeStore.closeResetStorageModal()
  }
}


</script>

<template>
  <div class="flex max-h-[93vh] w-full flex-col overflow-y-auto">
    <div class="flex w-full flex-col p-2">
      <h3 class="text-xl">Settings</h3>
    </div>
    <div class="flex w-full items-center justify-between p-2">
      <div class="flex items-center">Number of validators:</div>
      <div class="flex items-center text-xl font-semibold text-primary dark:text-white">
        {{ nodeStore.validators.length }}
      </div>
    </div>

    <div class="flex w-full flex-col bg-slate-100 p-2 dark:dark:bg-zinc-700">
      <h4 class="text-md" id="tutorial-validators">Validators Configuration</h4>
    </div>
    <div class="flex flex-col" id="tutorial-validators">
      <div class="flex w-full flex-col text-xs">
        <ValidatorItem
          v-for="validator in nodeStore.validators"
          :key="validator.id"
          :validator="validator"
        />
      </div>
    </div>
    <div class="mt-4 flex w-full flex-col px-2">
      <Btn @click="isNewValidatorModalOpen = true" data-testid="create-new-validator-btn">
        New Validator
      </Btn>
    </div>
    <div class="mt-10 flex w-full flex-col bg-slate-100 p-2 dark:dark:bg-zinc-700">
      <h4 class="text-md" id="tutorial-validators">Simulator Storage</h4>
    </div>
    <div class="mt-4 flex w-full flex-col px-2">
      <Btn
        @click="nodeStore.openResetStorageModal"
        :disabled="nodeStore.contractsToDelete.length < 1"
      >
        Reset Storage
      </Btn>
      <ToolTip
        text="No Contracts file to delete"
        :options="{ placement: 'right' }"
        v-if="nodeStore.contractsToDelete.length < 1"
      />
    </div>

    <NewValidatorModal
      :open="isNewValidatorModalOpen"
      @close="isNewValidatorModalOpen = false"
    />

    <ConfirmationModal
      :open="nodeStore.resetStorageModalOpen"
      @confirm="handleResetStorage"
      @close="nodeStore.closeResetStorageModal"
      :buttonText="'Reset Storage'"
      buttonTestId="btn-reset-storage"
      :dangerous="true"
      :confirming="nodeStore.resettingStorage"
    >
      <template #title>Reset Simulator Storage</template>
      <template #description
        >Are you sure? All the examples will be restored, and the following intelligent contracts
        will be removed.</template
      >

      <template #info>
        <div
          class="text-md font-semibold"
          v-for="contract in nodeStore.contractsToDelete"
          :key="contract.id"
        >
          {{ contract.name }}
        </div>
      </template>

      <div class="mt-1 text-xs italic">
        <span class="font-semibold">Note:</span> if you want to preserve any of these contracts,
        make a copy of them in the files section.
      </div>
    </ConfirmationModal>
  </div>
</template>
