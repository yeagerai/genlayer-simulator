<script setup lang="ts">
import { useNodeStore } from '@/stores'
import { type ValidatorModel, type CreateValidatorModel, type UpdateValidatorModel } from '@/types'
import { notify } from '@kyvg/vue3-notification'
import { computed, ref } from 'vue'

const nodeStore = useNodeStore()
const emit = defineEmits(['close'])

const props = defineProps<{
  validator?: ValidatorModel
}>()

const isCreateMode = computed(() => !props.validator)

async function handleCreateValidator() {
  try {
    await nodeStore.createNewValidator(newValidatorData.value)
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

async function handleUpdateValidator(validator: ValidatorModel) {
  try {
    await nodeStore.updateValidator(validator, newValidatorData.value)
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

// TODO: improve
const handleNumberInput = (event: Event) => {
  const formattedValue = parseInt((event?.target as any)?.value || '', 10)

  if (!isNaN(formattedValue)) {
    ;(event?.target as any).value = ''
    ;(event?.target as any).value = formattedValue
  } else {
    event.preventDefault()
  }
}

const newValidatorData = ref<CreateValidatorModel>({
  model: '',
  provider: '',
  stake: 1,
  config: '{ }',
})

const validatorModelValid = computed(() => {
  return (
    newValidatorData.value?.model !== '' &&
    newValidatorData.value?.provider !== '' &&
    newValidatorData.value?.stake > 0
  )
})

const providerOptions = computed(() => {
  return Object.keys(nodeStore.nodeProviders)
})

const handleChangeProvider = () => {
  newValidatorData.value.model = nodeStore.nodeProviders[newValidatorData.value.provider][0]
}

const tryInitValues = () => {
  if (!props.validator) {
    try {
      newValidatorData.value.provider = Object.keys(nodeStore.nodeProviders)[0]
      newValidatorData.value.model = nodeStore.nodeProviders[newValidatorData.value.provider][0]
    } catch (err) {
      console.error('Could not initialize values', err)
    }
  } else {
    newValidatorData.value = {
      model: props.validator.model,
      provider: props.validator.provider,
      stake: props.validator.stake,
      config: JSON.stringify(props.validator.config, null, 2),
    }
  }
}
</script>

<template>
  <Modal @close="emit('close')" @onOpen="tryInitValues">
    <template #title v-if="isCreateMode">Create New Validator</template>
    <template #title v-else>Update Validator</template>

    <template #info v-if="!isCreateMode">
      <div class="text-xs">
        <div>ID: {{ props.validator?.id }}</div>
        <div>Address: {{ props.validator?.address }}</div>
      </div>
    </template>

    <div>
      <FieldLabel for="provider">Provider:</FieldLabel>
      <SelectField
        name="provider"
        :options="providerOptions"
        v-model="newValidatorData.provider"
        @change="handleChangeProvider"
        :invalid="!newValidatorData.provider"
        testId="dropdown-provider-create"
      />
    </div>

    <div>
      <FieldLabel for="model">Model:</FieldLabel>
      <SelectField
        name="model"
        :options="nodeStore.nodeProviders[newValidatorData.provider] || []"
        v-model="newValidatorData.model"
        :invalid="!newValidatorData.model"
        testId="dropdown-model-create"
      />
    </div>

    <div>
      <FieldLabel for="stake">Stake:</FieldLabel>
      <NumberField
        name="stake"
        :min="1"
        :step="1"
        :invalid="newValidatorData.stake < 1"
        v-model="newValidatorData.stake"
        @input="handleNumberInput"
        required
        testId="input-stake-create"
      />
    </div>

    <div>
      <FieldLabel for="config">Config:</FieldLabel>
      <TextAreaField name="config" :rows="5" :cols="60" v-model="newValidatorData.config" />
    </div>

    <Btn
      v-if="isCreateMode"
      @click="handleCreateValidator"
      :disabled="!validatorModelValid"
      testId="btn-create-validator"
    >
      Create
    </Btn>

    <Btn
      v-if="!isCreateMode && validator"
      @click="handleUpdateValidator(validator)"
      :disabled="!validatorModelValid"
      testId="btn-update-validator"
    >
      Save
    </Btn>
  </Modal>
</template>
