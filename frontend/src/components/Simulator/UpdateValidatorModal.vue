<script setup lang="ts">
import { useNodeStore } from '@/stores'
import { type ValidatorModel, type UpdateValidatorModel } from '@/types'
import { notify } from '@kyvg/vue3-notification'
import { computed, ref } from 'vue'
const nodeStore = useNodeStore()

const props = defineProps<{
  validator: ValidatorModel
}>()
const emit = defineEmits(['close'])

async function handleUpdateValidator() {
  try {
    await nodeStore.updateValidator(props.validator, validatorToUpdate.value)
    notify({
      title: 'OK',
      text: 'Validator updated successfully',
      type: 'success',
    })
    emit('close')
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error udpating the validator',
      type: 'error',
    })
  }
}

// TODO: refac or improve
const handleNumberInput = (event: Event) => {
  const formattedValue = parseInt((event?.target as any)?.value || '', 10)

  if (!isNaN(formattedValue)) {
    ;(event?.target as any).value = ''
    ;(event?.target as any).value = formattedValue
  } else {
    event.preventDefault()
  }
}

const validatorToUpdate = ref<UpdateValidatorModel>({
  model: '',
  provider: '',
  stake: 0,
  config: '{ }',
})

const updateValidatorModelValid = computed(() => {
  return (
    validatorToUpdate.value?.model !== '' &&
    validatorToUpdate.value?.provider !== '' &&
    validatorToUpdate.value?.stake
  )
})
</script>

<template>
  <Modal @close="emit('close')">
    <template #title>Update Validator</template>
    <template #info>
      <div class="text-xs">
        ID: {{ validator.id }}
        Address: {{ validator.address }}
      </div>
    </template>


    
    <div class="flex flex-col">
      <div class="flex justify-between">
        <div class="text-xl">Validator Details</div>
        <div class="text-primary dark:text-white">ID: {{ validator.id }}</div>
      </div>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Address:</p>

        <div class="w-full py-2">
          {{ validator.address }}
        </div>
      </div>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Provider:</p>
        <select
          :class="validator.provider ? '' : 'border border-red-500'"
          data-testid="dropdown-provider-update"
          class="w-full overflow-y-auto bg-slate-100 p-2 dark:bg-zinc-700"
          v-model="validator.provider"
          required
        >
          <option
            v-for="(_, provider) in nodeStore.nodeProviders"
            :key="provider"
            :value="provider"
            :selected="provider === validator.provider"
          >
            {{ provider }}
          </option>
        </select>
      </div>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Model:</p>
        <select
          :class="validator.model ? '' : 'border border-red-500'"
          class="w-full overflow-y-auto bg-slate-100 p-2 dark:bg-zinc-700"
          name="dropdown-model"
          data-testid="dropdown-model-update"
          v-model="validator.model"
          required
        >
          <option
            v-for="model in nodeStore.nodeProviders[validator.provider]"
            :key="model"
            :value="model"
            :selected="model === validator.model"
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
          v-model="validator.stake"
          :class="validator.stake ? '' : 'border border-red-500'"
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
          v-model="validator.config"
        >
        </textarea>
      </div>
    </div>
    <div class="mt-4 flex w-full flex-col">
      <Btn
        @click="handleUpdateValidator"
        :disabled="!updateValidatorModelValid"
        data-testid="btn-update-validator"
      >
        Save
      </Btn>
    </div>
  </Modal>
</template>
