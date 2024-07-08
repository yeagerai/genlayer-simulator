<script setup lang="ts">
import { onMounted } from 'vue'
import { notify } from '@kyvg/vue3-notification'
import Modal from '@/components/ModalComponent.vue'
import { TrashIcon } from '@heroicons/vue/24/solid'
import { useNodeStore } from '@/stores'

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
      type: 'error'
    })
  }
})

async function handleCreateNewValidator() {
  try {
    await nodeStore.createNewValidator()
    notify({
      title: 'OK',
      text: 'New validator created',
      type: 'success'
    })
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error creating new validator',
      type: 'error'
    })
  }
}


async function handleUpdateValidator() {
  try {
    await nodeStore.updateValidator()
    notify({
      title: 'OK',
      text: 'Validator updated successfully',
      type: 'success'
    })
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error udpating the validator',
      type: 'error'
    })
  }
}

async function handleDeleteValidator() {
  try {
    await nodeStore.deleteValidator()
    notify({
      title: 'OK',
      text: 'Validator deleted successfully',
      type: 'success'
    })
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error deleting a validator',
      type: 'error'
    })
  }
}

const handleResetStorage = async () => {
  try {
    await nodeStore.resetStorage()
    notify({
      title: 'Success',
      text: 'Storage reset successfully',
      type: 'success'
    })
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error resetting the storage',
      type: 'error'
    })
  } finally {
   
    nodeStore.closeResetStorageModal()
  }
}
</script>

<template>
  <div class="flex flex-col overflow-y-auto max-h-[93vh] w-full">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Settings</h3>
    </div>
    <div class="flex justify-between items-center p-2 w-full">
      <div class="flex items-center">Number of validators:</div>
      <div class="flex items-center text-xl font-semibold dark:text-white text-primary">
        {{ nodeStore.validators.length }}
      </div>
    </div>

    <div class="flex flex-col p-2 w-full bg-slate-100 dark:dark:bg-zinc-700">
      <h4 class="text-md" id="tutorial-validators">Validators Configuration</h4>
    </div>
    <div class="flex flex-col" id="tutorial-validators">
      <div class="flex flex-col text-xs w-full">
        <div data-testid="validator-item-container"
          class="flex px-2 justify-between items-center hover:bg-slate-100 p-1 dark:hover:bg-zinc-700"
          v-for="validator in nodeStore.validators" :key="validator.id">
          <div class="flex items-center cursor-pointer" data-testid="validator-item" @click="nodeStore.openUpdateValidatorModal(validator)">
            <div class="flex dark:text-white text-primary">{{ validator.id }} -</div>
            <div class="flex flex-col items-start ml-2">
              <div class="flex">
                <span class="font-semibold mr-1">Model: </span>
                <span class="dark:text-white text-primary" data-testid="validator-item-model">{{ validator.model }}</span>
              </div>
              <div class="flex">
                <span class="font-semibold mr-1">Provider: </span>
                <span data-testid="validator-item-provider" >{{ validator.provider }}</span>
              </div>
            </div>
          </div>
          <div class="flex dark:text-white text-primary">
            <button @click="nodeStore.openDeleteValidatorModal(validator)" data-testid="validator-item-delete">
              <ToolTip text="Delete Validator" :options="{ placement: 'bottom' }" />
              <TrashIcon class="h-4 w-4 mr-1" />
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-col mt-4 w-full px-2">
      <button @click="nodeStore.openCreateNewValidatorModal" data-testid="create-new-validator-btn"
        class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
        New Validator
      </button>
    </div>
    <div class="mt-10 flex flex-col p-2 w-full bg-slate-100 dark:dark:bg-zinc-700">
      <h4 class="text-md" id="tutorial-validators">Simulator Storage</h4>
    </div>
    <div class="flex flex-col mt-4 w-full px-2">
      <button @click="nodeStore.openResetStorageModal"
        class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
        Reset Storage
      </button>
    </div>
    <Modal :open="nodeStore.updateValidatorModalOpen" @close="nodeStore.closeUpdateValidatorModal">
      <div class="flex flex-col">
        <div class="flex justify-between">
          <div class="text-xl">Validator Details</div>
          <div class="dark:text-white text-primary">ID: {{ nodeStore.selectedValidator?.id }}</div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Address:</p>

          <div class="py-2 w-full">
            {{ nodeStore.selectedValidator?.address }}
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Provider:</p>
          <select :class="nodeStore.validatorToUpdate.provider ? '' : 'border border-red-500'"
                  data-testid="dropdown-provider-update"
                  class="p-2 w-full bg-slate-100 dark:bg-zinc-700 overflow-y-auto"
                  v-model="nodeStore.validatorToUpdate.provider" required>
            <option v-for="(_, provider) in nodeStore.nodeProviders" :key="provider" :value="provider"
              :selected="provider === nodeStore.validatorToUpdate.provider">
              {{ provider }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Model:</p>
          <select :class="nodeStore.validatorToUpdate.model ? '' : 'border border-red-500'"
            class="p-2 w-full bg-slate-100 overflow-y-auto dark:bg-zinc-700" name="dropdown-model"
            data-testid="dropdown-model-update"
            v-model="nodeStore.validatorToUpdate.model" required>
            <option v-for="model in nodeStore.nodeProviders[nodeStore.validatorToUpdate.provider]" :key="model"
              :value="model" :selected="model === nodeStore.validatorToUpdate.model">
              {{ model }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Stake:</p>
          <input type="number" min="0.01" v-model="nodeStore.validatorToUpdate.stake"
            :class="nodeStore.validatorToUpdate.stake ? '' : 'border border-red-500'"
            data-testid="input-stake-update"
            class="p-2 w-full bg-slate-100 dark:bg-zinc-700" required />
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Config:</p>

          <textarea name="" id="" rows="5" cols="60" class="p-2 max-h-64 w-full bg-slate-100 dark:bg-zinc-700"
            v-model="nodeStore.validatorToUpdate.config">
          </textarea>
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleUpdateValidator" 
        :disabled="!nodeStore.updateValidatorModelValid"
          data-testid="btn-update-validator"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded disabled:opacity-80">
          Save
        </button>
      </div>
    </Modal>

    <Modal :open="nodeStore.createValidatorModalOpen" @close="nodeStore.closeNewValidatorModal">
      <div class="flex flex-col w-full">
        <div class="flex justify-between">
          <div class="text-xl">Create New Validator</div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Provider:</p>
          <select :class="nodeStore.validatorToCreate.provider ? '' : 'border border-red-500'"
            class="p-2 w-full bg-slate-100 dark:bg-zinc-700 overflow-y-auto" 
            data-testid="dropdown-provider-create"
            v-model="nodeStore.validatorToCreate.provider" required>
            <option v-for="(_, provider) in nodeStore.nodeProviders" :key="provider" :value="provider"
              :selected="provider === nodeStore.validatorToCreate.provider">
              {{ provider }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Model:</p>
          <select :class="nodeStore.validatorToCreate.model ? '' : 'border border-red-500'"
            class="p-2 w-full bg-slate-100 overflow-y-auto dark:bg-zinc-700" 
            data-testid="dropdown-model-create"
            v-model="nodeStore.validatorToCreate.model" required>
            <option v-for="model in nodeStore.nodeProviders[nodeStore.validatorToCreate.provider]" :key="model"
              :value="model" :selected="model === nodeStore.validatorToCreate.model">
              {{ model }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Stake:</p>
          <input type="number" min="0.01" 
            v-model="nodeStore.validatorToCreate.stake"
            data-testid="input-stake-create"
            :class="nodeStore.validatorToCreate.stake ? '' : 'border border-red-500'"
            class="p-2 w-full bg-slate-100 dark:bg-zinc-700" required />
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Config:</p>

          <textarea name="" id="" rows="5" cols="60" class="p-2 max-h-64 w-full bg-slate-100 dark:bg-zinc-700"
            v-model="nodeStore.validatorToCreate.config">
          </textarea>
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleCreateNewValidator" :disabled="!nodeStore.createValidatorModelValid"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded disabled:opacity-80"
          data-testid="btn-create-validator">
          Create
        </button>
      </div>
    </Modal>
    <Modal :open="nodeStore.deleteValidatorModalOpen" @close="nodeStore.closeDeleteValidatorModal">
      <div class="flex flex-col">
        <div class="flex justify-between">
          <div class="text-xl">Delete Validator</div>
          <div class="dark:text-white text-primary">ID: {{ nodeStore.selectedValidator?.id }}</div>
        </div>
        <div class="flex justify-between font-bold bg-slate-100 p-2 mt-4">
          Are you sure you want to delete this validator?
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Address:</p>

          <div class="py-2 w-full">
            {{ nodeStore.selectedValidator?.address }}
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Provider:</p>
          {{ nodeStore.selectedValidator?.provider }}
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Model:</p>
          {{ nodeStore.selectedValidator?.model }}
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Stake:</p>
          {{ nodeStore.selectedValidator?.stake }}
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleDeleteValidator"
        data-testid="btn-delete-validator"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
          Delete Validator
        </button>
      </div>
    </Modal>
    <Modal :open="nodeStore.resetStorageModalOpen" @close="nodeStore.closeResetStorageModal">
      <div class="flex flex-col">
        <div class="flex justify-between">
          <div class="text-xl">Reset Simulator Storage</div>
        </div>
        <div class="flex justify-between font-bold bg-slate-100 p-2 mt-4">
          Are you sure you want to reset the simulator storage?
        </div>
        <div class="flex flex-col p-2 mt-2">
          <div class="py-2 w-full">
            All the examples will be restored, and the following intelligent contracts will be removed.
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2 overflow-y-auto">
          <ul class="list-disc list-inside">
            <li class="text-md font-semibold" v-for="contract in nodeStore.contractsToDelete" :key="contract.id">
              {{ contract.name }}
            </li>
          </ul>
        </div>
        <div class="flex flex-col p-2 mt-2">
         <div class="text-md italic"><span class="font-semibold">Note:</span> if you want to preserve any of these contracts, make a copy of them in the files section.</div>
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleResetStorage"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
          <LoadingIndicator v-if="nodeStore.resetingStorage" :color="'white'">
          </LoadingIndicator>
          <span v-else>Reset</span>
        </button>
      </div>
    </Modal>
  </div>
</template>
