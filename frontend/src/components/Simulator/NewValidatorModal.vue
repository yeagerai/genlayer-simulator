<script setup lang="ts">
import { useNodeStore } from '@/stores'
import { type CreateValidatorModel } from '@/types'
import { notify } from '@kyvg/vue3-notification'
import { computed, ref } from 'vue'

const nodeStore = useNodeStore()
const emit = defineEmits(['close'])

const props = defineProps<{
  validator: ValidatorModel
}>()

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
  stake: 1,
  config: '{ }',
})

const createValidatorModelValid = computed(() => {
  return (
    validatorToCreate.value?.model !== '' &&
    validatorToCreate.value?.provider !== '' &&
    validatorToCreate.value?.stake
  )
})

const providerOptions = computed(() => {
  return Object.keys(nodeStore.nodeProviders)
})

const handleChangeProvider = () => {
  validatorToCreate.value.model = nodeStore.nodeProviders[validatorToCreate.value.provider][0]
}

const initValues = () => {
  try {
    validatorToCreate.value.provider = Object.keys(nodeStore.nodeProviders)[0]
    validatorToCreate.value.model = nodeStore.nodeProviders[validatorToCreate.value.provider][0]
  } catch (err) {
    console.error('Could not initialize values', err)
  }
}
</script>

<template>
  <Modal @close="emit('close')" @onOpen="initValues">
    <template #title>Create New Validator</template>

    <div>
      <FieldLabel for="provider">Provider:</FieldLabel>
      <SelectField
        name="provider"
        :options="providerOptions"
        v-model="validatorToCreate.provider"
        @change="handleChangeProvider"
        :invalid="!validatorToCreate.provider"
        testId="dropdown-provider-create"
      />
    </div>

    <div>
      <FieldLabel for="model">Model:</FieldLabel>
      <SelectField
        name="model"
        :options="nodeStore.nodeProviders[validatorToCreate.provider] || []"
        v-model="validatorToCreate.model"
        :invalid="!validatorToCreate.model"
        testId="dropdown-model-create"
      />
    </div>

    <div>
      <FieldLabel for="stake">Stake:</FieldLabel>
      <NumberField
        name="stake"
        :min="1"
        :step="1"
        :invalid="validatorToCreate.stake < 1"
        v-model="validatorToCreate.stake"
        @input="handleNumberInput"
        required
        testId="input-stake-create"
      />
    </div>

    <div>
      <FieldLabel for="config">Config:</FieldLabel>
      <TextAreaField name="config" :rows="5" :cols="60" v-model="validatorToCreate.config" />
    </div>

    <Btn
      @click="handleCreateNewValidator"
      :disabled="!createValidatorModelValid"
      data-testid="btn-create-validator"
    >
      Create
    </Btn>
  </Modal>
</template>
