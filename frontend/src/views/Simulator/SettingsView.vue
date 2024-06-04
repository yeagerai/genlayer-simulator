<script setup lang="ts">
import type { ValidatorModel, UpdateValidatorModel, CreateValidatorModel } from '@/types'

import { inject, onMounted, ref } from 'vue'
import { notify } from '@kyvg/vue3-notification'
import Modal from '@/components/ModalComponent.vue'
import { TrashIcon } from '@heroicons/vue/24/solid'
import type { IJsonRPCService } from '@/services'
import { useMainStore } from '@/stores'
import { setupStores } from '@/utils'

const mainStore = useMainStore()
const nodeProviders = ref<Record<string, string[]>>({})
// state
const $jsonRpc = inject<IJsonRPCService>('$jsonRpc')!
const validators = ref<ValidatorModel[]>([])
const updateValidatorModalOpen = ref<boolean>(false)
const createValidatorModalOpen = ref<boolean>(false)
const deleteValidatorModalOpen = ref<boolean>(false)
const resetStorageModalOpen = ref<boolean>(false)
const resetingStorage = ref<boolean>(false)
const selectedValidator = ref<ValidatorModel>()
const validatorToUpdate = ref<UpdateValidatorModel>({
  model: '',
  provider: '',
  stake: 0,
  config: '{ }'
})
const validatorToCreate = ref<CreateValidatorModel>({
  model: '',
  provider: '',
  stake: 0,
  config: '{ }'
})

// Hooks
onMounted(async () => {
  try {

    const [{ result: validatorsResult }, { result: modelsResult }] = await Promise.all([$jsonRpc.call({
      method: 'get_all_validators',
      params: []
    }), $jsonRpc.call({
      method: 'get_providers_and_models',
      params: []
    })])

    
    if (validatorsResult?.status === 'success') {
      validators.value = validatorsResult.data
    } else {
      notify({
        title: 'Error',
        text: 'Error getting validators',
        type: 'error'
      })
    }

    if (modelsResult?.status === 'success') {
      nodeProviders.value = modelsResult.data
    } else {
      notify({
        title: 'Error',
        text: 'Error getting Providers and Models data',
        type: 'error'
      })
    }
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: 'Error getting validators',
      type: 'error'
    })
  }
})

const openDeleteValidatorModal = (validator: ValidatorModel) => {
  selectedValidator.value = validator
  deleteValidatorModalOpen.value = true
}

const openUpdateValidatorModal = (validator: ValidatorModel) => {
  selectedValidator.value = validator
  const { model, provider, stake, config } = validator
  validatorToUpdate.value = {
    model,
    provider,
    stake,
    config: JSON.stringify(config || '{ }', null, 2)
  }
  updateValidatorModalOpen.value = true
}

const closeUpdateValidatorModal = () => {
  selectedValidator.value = undefined
  updateValidatorModalOpen.value = false
  validatorToUpdate.value = {
    model: '',
    provider: '',
    stake: 0,
    config: '{ }'
  }
}

const closeDeleteValidatorModal = () => {
  selectedValidator.value = undefined
  deleteValidatorModalOpen.value = false
}

const handleUpdateValidator = async () => {
  try {
    const { stake, provider, model, config } = validatorToUpdate.value

    if (stake <= 0 || !provider || !model || !config) {
      notify({
        title: 'Error',
        text: 'Please fill all the required fields',
        type: 'warning'
      })
      return
    }
    const contractConfig = JSON.parse(config || '{}')
    const { result } = await $jsonRpc.call({
      method: 'update_validator',
      params: [selectedValidator.value?.address, stake, provider, model, contractConfig]
    })
    if (result?.status === 'success') {
      const index = validators.value.findIndex(
        (v) => v.address === selectedValidator.value?.address
      )

      if (index >= 0) {
        validators.value.splice(index, 1, result.data)
      }
      notify({
        title: 'Success',
        text: 'Validator updated successfully',
        type: 'success'
      })
      closeUpdateValidatorModal()
    } else {
      notify({
        title: 'Error',
        text: 'Error udpating the validator',
        type: 'error'
      })
    }
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: 'Error udpating the validator',
      type: 'error'
    })
  }
}

const handleDeleteValidator = async () => {
  const address = selectedValidator.value?.address
  try {
    if (validators.value.length === 1) {
      notify({
        title: 'Error',
        text: 'You must have at least one validator',
        type: 'error'
      })
      return
    }
    const { result } = await $jsonRpc.call({
      method: 'delete_validator',
      params: [address]
    })
    if (result?.status === 'success') {
      validators.value = validators.value.filter((v) => v.address !== address)
    } else {
      notify({
        title: 'Error',
        text: 'Error deleting a validator',
        type: 'error'
      })
    }

    closeDeleteValidatorModal()
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: 'Error deleting a validator',
      type: 'error'
    })
  }
}

const openCreateNewValidatorModal = async () => {
  createValidatorModalOpen.value = true
}

const closeNewValidatorModal = () => {
  createValidatorModalOpen.value = false
  validatorToCreate.value = {
    model: '',
    provider: '',
    stake: 0,
    config: '{ }'
  }
}
const handleCreateNewValidator = async () => {
  try {
    if (!validatorToCreate.value.stake) {
      notify({
        title: 'Error',
        text: 'Please fill the stake field',
        type: 'warning'
      })
      return
    }
    const { stake, provider, model, config } = validatorToCreate.value
    const { result } = await $jsonRpc.call({
      method: 'create_validator',
      params: [stake, provider, model, config]
    })
    if (result?.status === 'success') {
      validators.value.push(result.data)
      notify({
        title: 'Success',
        text: 'New Validator created successfully',
        type: 'success'
      })
      closeNewValidatorModal()
    } else {
      notify({
        title: 'Error',
        text: 'Error creating a new validator',
        type: 'error'
      })
    }
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: 'Error creating a new validator',
      type: 'error'
    })
  }
}

const openResetStorageModal = () => {
  resetStorageModalOpen.value = true
}

const closeResetStorageModal = () => {
  resetStorageModalOpen.value = false
}

const handleResetStorage = async () => {
  resetingStorage.value = true
  try {
    await mainStore.resetStorage()
    await setupStores()
    notify({
        title: 'Success',
        text: 'Storage reset successfully',
        type: 'success'
      })
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: 'Error resetting the storage',
      type: 'error'
    })
  } finally {
    resetingStorage.value = false
    closeResetStorageModal()
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
        {{ validators.length }}
      </div>
    </div>
    
    <div class="flex flex-col p-2 w-full bg-slate-100 dark:dark:bg-zinc-700">
      <h4 class="text-md" id="tutorial-validators">Validators Configuration</h4>
    </div>
    <div class="flex flex-col" id="tutorial-validators">
      <div class="flex flex-col text-xs w-full">
        <div class="flex px-2 justify-between items-center hover:bg-slate-100 p-1 dark:hover:bg-zinc-700"
          v-for="validator in validators" :key="validator.id">
          <div class="flex items-center cursor-pointer" @click="openUpdateValidatorModal(validator)">
            <div class="flex dark:text-white text-primary">{{ validator.id }} -</div>
            <div class="flex flex-col items-start ml-2">
              <div class="flex">
                <span class="font-semibold mr-1">Model: </span>
                <span class="dark:text-white text-primary">{{ validator.model }}</span>
              </div>
              <div class="flex">
                <span class="font-semibold mr-1">Provider: </span>
                <span>{{ validator.provider }}</span>
              </div>
            </div>
          </div>
          <div class="flex dark:text-white text-primary">
            <button @click="openDeleteValidatorModal(validator)">
              <ToolTip text="Delete Validator" :options="{ placement: 'bottom' }" />
              <TrashIcon class="h-4 w-4 mr-1" />
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-col mt-4 w-full px-2">
      <button @click="openCreateNewValidatorModal"
        class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
        New Validator
      </button>
    </div>
    <div class="mt-10 flex flex-col p-2 w-full bg-slate-100 dark:dark:bg-zinc-700">
      <h4 class="text-md" id="tutorial-validators">Simulator Storage</h4>
    </div>
    <div class="flex flex-col mt-4 w-full px-2">
      <button @click="openResetStorageModal"
        class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
        Reset Storage
      </button>
    </div>
    <Modal :open="updateValidatorModalOpen" @close="closeUpdateValidatorModal">
      <div class="flex flex-col">
        <div class="flex justify-between">
          <div class="text-xl">Validator Details</div>
          <div class="dark:text-white text-primary">ID: {{ selectedValidator?.id }}</div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Address:</p>

          <div class="py-2 w-full">
            {{ selectedValidator?.address }}
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Provider:</p>
          <select class="p-2 w-full bg-slate-100 dark:bg-zinc-700 overflow-y-auto" name="" id=""
            v-model="validatorToUpdate.provider">
            <option v-for="(_, provider) in nodeProviders" :key="provider" :value="provider"
              :selected="provider === validatorToUpdate.provider">
              {{ provider }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Model:</p>
          <select class="p-2 w-full bg-slate-100 overflow-y-auto dark:bg-zinc-700" name="" id=""
            v-model="validatorToUpdate.model">
            <option v-for="model in nodeProviders[validatorToUpdate.provider]" :key="model" :value="model"
              :selected="model === validatorToUpdate.model">
              {{ model }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Stake:</p>
          <input type="number" min="0.01" v-model="validatorToUpdate.stake"
            class="p-2 w-full bg-slate-100 dark:bg-zinc-700" required />
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Config:</p>

          <textarea name="" id="" rows="5" cols="60" class="p-2 max-h-64 w-full bg-slate-100 dark:bg-zinc-700"
            v-model="validatorToUpdate.config">
          </textarea>
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleUpdateValidator"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
          Save
        </button>
      </div>
    </Modal>

    <Modal :open="createValidatorModalOpen" @close="closeNewValidatorModal">
      <div class="flex flex-col w-full">
        <div class="flex justify-between">
          <div class="text-xl">Create New Validator</div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Provider:</p>
          <select class="p-2 w-full bg-slate-100 dark:bg-zinc-700 overflow-y-auto" name="" id=""
            v-model="validatorToCreate.provider">
            <option v-for="(_, provider) in nodeProviders" :key="provider" :value="provider"
              :selected="provider === validatorToCreate.provider">
              {{ provider }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Model:</p>
          <select class="p-2 w-full bg-slate-100 overflow-y-auto dark:bg-zinc-700" name="" id=""
            v-model="validatorToCreate.model">
            <option v-for="model in nodeProviders[validatorToCreate.provider]" :key="model" :value="model"
              :selected="model === validatorToCreate.model">
              {{ model }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Stake:</p>
          <input type="number" min="0.01" v-model="validatorToCreate.stake"
            class="p-2 w-full bg-slate-100 dark:bg-zinc-700" required />
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Config:</p>

          <textarea name="" id="" rows="5" cols="60" class="p-2 max-h-64 w-full bg-slate-100 dark:bg-zinc-700"
            v-model="validatorToCreate.config">
          </textarea>
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleCreateNewValidator"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
          Create
        </button>
      </div>
    </Modal>
    <Modal :open="deleteValidatorModalOpen" @close="closeDeleteValidatorModal">
      <div class="flex flex-col">
        <div class="flex justify-between">
          <div class="text-xl">Delete Validator</div>
          <div class="dark:text-white text-primary">ID: {{ selectedValidator?.id }}</div>
        </div>
        <div class="flex justify-between font-bold bg-slate-100 p-2 mt-4">
          Are you sure you want to delete this validator?
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Address:</p>

          <div class="py-2 w-full">
            {{ selectedValidator?.address }}
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Provider:</p>
          {{ selectedValidator?.provider }}
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Model:</p>
          {{ selectedValidator?.model }}
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Stake:</p>
          {{ selectedValidator?.stake }}
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleDeleteValidator"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
          Delete Validator
        </button>
      </div>
    </Modal>
    <Modal :open="resetStorageModalOpen" @close="closeResetStorageModal">
      <div class="flex flex-col">
        <div class="flex justify-between">
          <div class="text-xl">Reset Simulator Storage</div>
        </div>
        <div class="flex justify-between font-bold bg-slate-100 p-2 mt-4">
          Are you sure you want to reset the simulator storage?
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleResetStorage"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">
          <LoadingIndicator v-if="resetingStorage" :color="'white'">
          </LoadingIndicator>
          <span v-else>Reset</span>
        </button>
      </div>
    </Modal>
  </div>
</template>
