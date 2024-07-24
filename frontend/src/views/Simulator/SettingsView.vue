<script setup lang="ts">
import { onMounted } from 'vue'
import { notify } from '@kyvg/vue3-notification'
import { TrashIcon } from '@heroicons/vue/24/solid'
import { useNodeStore } from '@/stores'
import ConfirmationModal from '@/components/global/ConfirmationModal.vue'

const nodeStore = useNodeStore()

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

async function handleCreateNewValidator() {
  try {
    await nodeStore.createNewValidator()
    notify({
      title: 'OK',
      text: 'New validator created',
      type: 'success',
    })
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error creating new validator',
      type: 'error',
    })
  }
}

async function handleUpdateValidator() {
  try {
    await nodeStore.updateValidator()
    notify({
      title: 'OK',
      text: 'Validator updated successfully',
      type: 'success',
    })
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error udpating the validator',
      type: 'error',
    })
  }
}

async function handleDeleteValidator() {
  try {
    await nodeStore.deleteValidator()
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
  }
}

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

const handleNumberInput = (event: Event) => {
  const formattedValue = parseInt((event?.target as any)?.value || '', 10)

  if (!isNaN(formattedValue)) {
    ;(event?.target as any).value = ''
    ;(event?.target as any).value = formattedValue
  } else {
    event.preventDefault()
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
        <div
          data-testid="validator-item-container"
          class="flex items-center justify-between p-1 px-2 hover:bg-slate-100 dark:hover:bg-zinc-700"
          v-for="validator in nodeStore.validators"
          :key="validator.id"
        >
          <div
            class="flex cursor-pointer items-center"
            data-testid="validator-item"
            @click="nodeStore.openUpdateValidatorModal(validator)"
          >
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
          <div class="flex text-primary dark:text-white">
            <button
              @click="nodeStore.openDeleteValidatorModal(validator)"
              data-testid="validator-item-delete"
            >
              <ToolTip text="Delete Validator" :options="{ placement: 'bottom' }" />
              <TrashIcon class="mr-1 h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-4 flex w-full flex-col px-2">
      <Btn @click="nodeStore.openCreateNewValidatorModal" data-testid="create-new-validator-btn">
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
    <Modal :open="nodeStore.createValidatorModalOpen" @close="nodeStore.closeNewValidatorModal">
      <template #title>Create New Validator</template>
      <!-- <template #description>Create New Validator</template> -->

      <div class="flex w-full flex-col">
        <!-- <div class="flex justify-between">
          <div class="text-xl">Create New Validator</div>
        </div> -->
        <div class="mt-2 flex flex-col p-2">
          <p class="text-md font-semibold">Provider:</p>
          <select
            :class="nodeStore.validatorToCreate.provider ? '' : 'border border-red-500'"
            class="w-full overflow-y-auto bg-slate-100 p-2 dark:bg-zinc-700"
            data-testid="dropdown-provider-create"
            v-model="nodeStore.validatorToCreate.provider"
            required
          >
            <option
              v-for="(_, provider) in nodeStore.nodeProviders"
              :key="provider"
              :value="provider"
              :selected="provider === nodeStore.validatorToCreate.provider"
            >
              {{ provider }}
            </option>
          </select>
        </div>
        <div class="mt-2 flex flex-col p-2">
          <p class="text-md font-semibold">Model:</p>
          <select
            :class="nodeStore.validatorToCreate.model ? '' : 'border border-red-500'"
            class="w-full overflow-y-auto bg-slate-100 p-2 dark:bg-zinc-700"
            data-testid="dropdown-model-create"
            v-model="nodeStore.validatorToCreate.model"
            required
          >
            <option
              v-for="model in nodeStore.nodeProviders[nodeStore.validatorToCreate.provider]"
              :key="model"
              :value="model"
              :selected="model === nodeStore.validatorToCreate.model"
            >
              {{ model }}
            </option>
          </select>
        </div>
        <div class="mt-2 flex flex-col p-2">
          <p class="text-md font-semibold">Stake:</p>
          <input
            type="number"
            min="1"
            step="1"
            data-testid="input-stake-create"
            @input="handleNumberInput"
            v-model="nodeStore.validatorToCreate.stake"
            :class="nodeStore.validatorToCreate.stake ? '' : 'border border-red-500'"
            class="w-full bg-slate-100 p-2 dark:bg-zinc-700"
            required
          />
        </div>
        <div class="mt-2 flex flex-col p-2">
          <p class="text-md font-semibold">Config:</p>

          <textarea
            name=""
            id=""
            rows="5"
            cols="60"
            class="max-h-64 w-full bg-slate-100 p-2 dark:bg-zinc-700"
            v-model="nodeStore.validatorToCreate.config"
          >
          </textarea>
        </div>
      </div>
      <div class="mt-4 flex w-full flex-col">
        <Btn
          @click="handleCreateNewValidator"
          :disabled="!nodeStore.createValidatorModelValid"
          data-testid="btn-create-validator"
        >
          Create
        </Btn>
      </div>
    </Modal>
    <Modal :open="nodeStore.updateValidatorModalOpen" @close="nodeStore.closeUpdateValidatorModal">
      <div class="flex flex-col">
        <div class="flex justify-between">
          <div class="text-xl">Validator Details</div>
          <div class="text-primary dark:text-white">ID: {{ nodeStore.selectedValidator?.id }}</div>
        </div>
        <div class="mt-2 flex flex-col p-2">
          <p class="text-md font-semibold">Address:</p>

          <div class="w-full py-2">
            {{ nodeStore.selectedValidator?.address }}
          </div>
        </div>
        <div class="mt-2 flex flex-col p-2">
          <p class="text-md font-semibold">Provider:</p>
          <select
            :class="nodeStore.validatorToUpdate.provider ? '' : 'border border-red-500'"
            data-testid="dropdown-provider-update"
            class="w-full overflow-y-auto bg-slate-100 p-2 dark:bg-zinc-700"
            v-model="nodeStore.validatorToUpdate.provider"
            required
          >
            <option
              v-for="(_, provider) in nodeStore.nodeProviders"
              :key="provider"
              :value="provider"
              :selected="provider === nodeStore.validatorToUpdate.provider"
            >
              {{ provider }}
            </option>
          </select>
        </div>
        <div class="mt-2 flex flex-col p-2">
          <p class="text-md font-semibold">Model:</p>
          <select
            :class="nodeStore.validatorToUpdate.model ? '' : 'border border-red-500'"
            class="w-full overflow-y-auto bg-slate-100 p-2 dark:bg-zinc-700"
            name="dropdown-model"
            data-testid="dropdown-model-update"
            v-model="nodeStore.validatorToUpdate.model"
            required
          >
            <option
              v-for="model in nodeStore.nodeProviders[nodeStore.validatorToUpdate.provider]"
              :key="model"
              :value="model"
              :selected="model === nodeStore.validatorToUpdate.model"
            >
              {{ model }}
            </option>
          </select>
        </div>
        <div class="mt-2 flex flex-col p-2">
          <p class="text-md font-semibold">Stake:</p>
          <input
            type="number"
            min="1"
            step="1"
            @input="handleNumberInput"
            v-model="nodeStore.validatorToUpdate.stake"
            :class="nodeStore.validatorToUpdate.stake ? '' : 'border border-red-500'"
            data-testid="input-stake-update"
            class="w-full bg-slate-100 p-2 dark:bg-zinc-700"
            required
          />
        </div>
        <div class="mt-2 flex flex-col p-2">
          <p class="text-md font-semibold">Config:</p>

          <textarea
            name=""
            id=""
            rows="5"
            cols="60"
            class="max-h-64 w-full bg-slate-100 p-2 dark:bg-zinc-700"
            v-model="nodeStore.validatorToUpdate.config"
          >
          </textarea>
        </div>
      </div>
      <div class="mt-4 flex w-full flex-col">
        <Btn
          @click="handleUpdateValidator"
          :disabled="!nodeStore.updateValidatorModelValid"
          data-testid="btn-update-validator"
        >
          Save
        </Btn>
      </div>
    </Modal>

    <ConfirmationModal
      :open="nodeStore.deleteValidatorModalOpen"
      @confirm="handleDeleteValidator"
      @close="nodeStore.closeDeleteValidatorModal"
      :buttonText="`Delete Validator #${nodeStore.selectedValidator?.id}`"
      buttonTestId="btn-delete-validator"
    >
      <template #title>Delete Validator</template>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Address:</p>

        <div class="w-full py-2">
          {{ nodeStore.selectedValidator?.address }}
        </div>
      </div>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Provider:</p>
        {{ nodeStore.selectedValidator?.provider }}
      </div>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Model:</p>
        {{ nodeStore.selectedValidator?.model }}
      </div>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Stake:</p>
        {{ nodeStore.selectedValidator?.stake }}
      </div>
    </ConfirmationModal>

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
