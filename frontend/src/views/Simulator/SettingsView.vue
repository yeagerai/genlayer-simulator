<script setup lang="ts">
import type { ValidatorModel, UpdateValidatorModel, CreateValidatorModel } from '@/types';
import { rpcClient } from '@/utils';
import { onMounted, ref } from 'vue';
import { notify } from "@kyvg/vue3-notification";
import Modal from '@/components/ModalComponent.vue'
import { shortenAddress } from '@/utils'
import { TrashIcon } from '@heroicons/vue/24/solid'

const models = ['llama2', 'gemma', 'mistral', 'mixtral', 'gpt-4']
const providers = ['openai']
// state
const validators = ref<ValidatorModel[]>([])
const updateValidatorModalOpen = ref<boolean>(false)
const createValidatorModalOpen = ref<boolean>(false)
const selectedValidator = ref<ValidatorModel>()
const validatorToUpdate = ref<UpdateValidatorModel>({
  model: '',
  provider: '',
  stake: 0,
  config: '{ }'
})
const validatorToCreate = ref<CreateValidatorModel>({
  stake: 0,
})

// Hooks
onMounted(async () => {

  try {
    const { result } = await rpcClient.call({
      method: 'get_all_validators',
      params: []
    })
    if (result?.status === 'success') {
      validators.value = result.data
    } else {
      notify({
        title: 'Error',
        text: 'Error getting validators',
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

const handleSelectValidator = (validator: ValidatorModel) => {
  selectedValidator.value = validator
  const { model,
    provider,
    stake, config } = validator
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

const handleUpdateValidator = async () => {
  try {
    //validator_address: str, stake: float, provider: str, model: str, config
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
    const { result } = await rpcClient.call({
      method: 'update_validator',
      params: [selectedValidator.value?.address, stake, provider, model, contractConfig] //TODO: replace with a input for the stake
    })
    if (result?.status === 'success') {

      const index = validators.value.findIndex(v => v.address === selectedValidator.value?.address)

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

const handleDeleteValidator = async (address: string) => {
  try {
    if (validators.value.length === 1) {
      notify({
        title: 'Error',
        text: 'You must have at least one validator',
        type: 'error'
      })
      return
    }
    const { result } = await rpcClient.call({
      method: 'delete_validator',
      params: [address]
    })
    if (result?.status === 'success') {
      validators.value = validators.value.filter(v => v.address !== address)
    } else {
      notify({
        title: 'Error',
        text: 'Error deleting a validator',
        type: 'error'
      })
    }
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
    stake: 0
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
    const { result } = await rpcClient.call({
      method: 'create_random_validator',
      params: [validatorToCreate.value.stake] //TODO: replace with a input for the stake
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
</script>

<template>
  <div class="flex flex-col overflow-y-auto max-h-[93vh] w-full">
    <div class="flex flex-col p-2 w-full">
      <h3 class="text-xl">Settings</h3>
    </div>
    <div class="flex justify-between items-center p-2 w-full">
      <div class="flex items-center">
        Number of validators:
      </div>
      <div class="flex items-center text-xl font-semibold text-primary">
        {{ validators.length }}
      </div>
    </div>
    <div class="flex flex-col p-2 w-full">
      <h4 class="text-md">Validators Configuration</h4>
    </div>
    <div class="flex flex-col">
      <div class="flex flex-col text-xs w-full">
        <div class="flex px-2 justify-between items-center hover:bg-slate-100 p-1" v-for="validator in validators"
          :key="validator.id">
          <div class="flex items-center cursor-pointer" @click="handleSelectValidator(validator)">
            <div class="flex text-primary">{{ validator.id }} - </div>
            <div class="flex flex-col items-start ml-2">
              <div class="flex"><span class="font-semibold mr-1">Model: </span> <span class="text-primary">{{
          validator.model }}</span></div>
              <div class="flex"><span class="font-semibold mr-1">Provider: </span> <span>{{ validator.provider }}</span>
              </div>
            </div>
            <div class="flex text-primary pl-4 pr-2">
              {{ shortenAddress(validator.address) }}
            </div>
          </div>
          <div class="flex text-primary">
            <button @click="handleDeleteValidator(validator.address)">
              <ToolTip text="Delete Validator" :options="{ placement: 'bottom' }" />
              <TrashIcon class="h-4 w-4 mr-1" />
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-col mt-4 w-full px-2">
      <button @click="openCreateNewValidatorModal"
        class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">New Validator</button>
    </div>
    <Modal :open="updateValidatorModalOpen" @close="closeUpdateValidatorModal">
      <div class="flex flex-col">
        <div class="flex justify-between">
          <div class="text-xl">Validator Details</div>
          <div class="text-primary">ID: {{ selectedValidator?.id }}</div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Address:</p>

          <div class="py-2 w-full">
            {{ selectedValidator?.address }}
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Model:</p>
          <select class="p-2 w-full bg-slate-100 overflow-y-auto" name="" id="" v-model="validatorToUpdate.model">
            <option v-for="model in models" :key="model" :value="model">
              {{ model }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Provider:</p>
          <select class="p-2 w-full bg-slate-100 overflow-y-auto" name="" id="" v-model="validatorToUpdate.provider">
            <option v-for="provider in providers" :key="provider" :value="provider">
              {{ provider }}
            </option>
          </select>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Stake:</p>
          <input type="number" min="0.01" v-model="validatorToUpdate.stake" class="p-2 w-full bg-slate-100" required />
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Config:</p>

          <textarea name="" id="" rows="5" cols="60" class="p-2 max-h-64 w-full bg-slate-100"
            v-model="validatorToUpdate.config">

          </textarea>
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleUpdateValidator"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">Save</button>
      </div>
    </Modal>
    <Modal :open="createValidatorModalOpen" @close="closeNewValidatorModal">
      <div class="flex flex-col w-full">
        <div class="flex justify-between">
          <div class="text-xl">Create New Validator</div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Stake:</p>
          <input type="number" min="0.01" v-model="validatorToCreate.stake" class="p-2 w-full bg-slate-100" required />
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleCreateNewValidator"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">Create</button>
      </div>
    </Modal>
  </div>
</template>
