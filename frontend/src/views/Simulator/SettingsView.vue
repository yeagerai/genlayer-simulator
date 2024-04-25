<script setup lang="ts">
import type { ValidatorRecord } from '@/types';
import { rpcClient } from '@/utils';
import { onMounted, ref, watch } from 'vue';
import { notify } from "@kyvg/vue3-notification";
import Modal from '@/components/ModalComponent.vue'
import { shortenAddress } from '@/utils'
import { TrashIcon } from '@heroicons/vue/24/solid'
const validators = ref<ValidatorRecord[]>([])
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

const selectedValidator = ref<ValidatorRecord>()
const validatorConfig = ref('')
const handleSelectValidator = (validator: ValidatorRecord) => {
  selectedValidator.value = validator
}

const handleCloseModal = () => {
  selectedValidator.value = undefined
}

const handleUpdateValidator = async () => {

}

const handleDeleteValidator = async (address: string) => {
  try {
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
const handleCreateNewValidator = async () => {
  try {
    const { result } = await rpcClient.call({
      method: 'create_random_validator',
      params: [7] //TODO: replace with a input for the stake
    })
    if (result?.status === 'success') {
      validators.value.push(result.data)
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
watch(() => selectedValidator.value, async (newValue) => {
  if (newValue) {
    validatorConfig.value = JSON.stringify(newValue.config, null, 2)
  }
})
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
      <button @click="handleCreateNewValidator"
        class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">Create new Validator</button>
    </div>
    <Modal :open="true" @close="handleCloseModal" v-if="selectedValidator">
      <div class="flex flex-col">
        <div class="flex justify-between">
          <div class="text-xl">Validator Details</div>
          <div class="text-primary">ID: {{ selectedValidator?.id }}</div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Address:</p>

          <div class="p-2 w-full bg-slate-100 overflow-y-auto">
            {{ selectedValidator?.address }}
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Model:</p>

          <div class="p-2 w-full bg-slate-100 overflow-y-auto">
            {{ selectedValidator?.model }}
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Provider:</p>

          <div class="p-2 w-full bg-slate-100 overflow-y-auto">
            {{ selectedValidator?.provider }}
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Stake:</p>

          <div class="p-2 w-full bg-slate-100 overflow-y-auto">
            {{ selectedValidator?.stake }}
          </div>
        </div>
        <div class="flex flex-col p-2 mt-2">
          <p class="text-md font-semibold">Config:</p>

          <textarea name="" id="" rows="5" cols="60" class="p-2 max-h-64 w-full bg-slate-100" v-model="validatorConfig">

          </textarea>
        </div>
      </div>
      <div class="flex flex-col mt-4 w-full">
        <button @click="handleUpdateValidator"
          class="bg-primary hover:opacity-80 text-white font-semibold px-4 py-2 rounded">Save</button>
      </div>
    </Modal>
  </div>
</template>
