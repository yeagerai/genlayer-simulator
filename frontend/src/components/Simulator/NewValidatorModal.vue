<script setup lang="ts">
import { useNodeStore } from '@/stores'
import { type ValidatorModel, type CreateValidatorModel } from '@/types'
import { notify } from '@kyvg/vue3-notification'
import { computed, ref } from 'vue'

const nodeStore = useNodeStore()
const emit = defineEmits(['close'])

async function handleCreateNewValidator() {
  try {
    await nodeStore.createNewValidator(validatorToCreate.value)
    notify({
      title: 'OK',
      text: 'New validator created',
      type: 'success',
    })
    emit('close')   
  } catch (error) {
    console.error(error)
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error creating new validator',
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

const validatorToCreate = ref<CreateValidatorModel>({
  model: '',
  provider: '',
  stake: 0,
  config: '{ }',
})

const createValidatorModelValid = computed(() => {
  return (
    validatorToCreate.value?.model !== '' &&
    validatorToCreate.value?.provider !== '' &&
    validatorToCreate.value?.stake
  )
})
</script>

<template>
  <Modal @close="emit('close')">
    <template #title>Create New Validator</template>
    <!-- <template #description>Create New Validator</template> -->

    <div class="flex w-full flex-col">
      <!-- <div class="flex justify-between">
        <div class="text-xl">Create New Validator</div>
      </div> -->
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Provider:</p>
        <select
          :class="validatorToCreate.provider ? '' : 'border border-red-500'"
          class="w-full overflow-y-auto bg-slate-100 p-2 dark:bg-zinc-700"
          data-testid="dropdown-provider-create"
          v-model="validatorToCreate.provider"
          required
        >
          <option
            v-for="(_, provider) in nodeStore.nodeProviders"
            :key="provider"
            :value="provider"
            :selected="provider === validatorToCreate.provider"
          >
            {{ provider }}
          </option>
        </select>
      </div>
      <div class="mt-2 flex flex-col p-2">
        <p class="text-md font-semibold">Model:</p>
        <select
          :class="validatorToCreate.model ? '' : 'border border-red-500'"
          class="w-full overflow-y-auto bg-slate-100 p-2 dark:bg-zinc-700"
          data-testid="dropdown-model-create"
          v-model="validatorToCreate.model"
          required
        >
          <option
            v-for="model in nodeStore.nodeProviders[validatorToCreate.provider]"
            :key="model"
            :value="model"
            :selected="model === validatorToCreate.model"
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
          v-model="validatorToCreate.stake"
          :class="validatorToCreate.stake ? '' : 'border border-red-500'"
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
          v-model="validatorToCreate.config"
        >
        </textarea>
      </div>
    </div>
    <div class="mt-4 flex w-full flex-col">
      <Btn
        @click="handleCreateNewValidator"
        :disabled="!createValidatorModelValid"
        data-testid="btn-create-validator"
      >
        Create
      </Btn>
    </div>
  </Modal>
</template>
