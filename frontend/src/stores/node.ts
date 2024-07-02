import type { IJsonRpcService } from '@/services'
import type { CreateValidatorModel, NodeLog, UpdateValidatorModel, ValidatorModel } from '@/types'
import { webSocketClient } from '@/utils'
import { defineStore } from 'pinia'
import { computed, inject, ref } from 'vue'

export const useNodeStore = defineStore('nodeStore', () => {
  const logs = ref<NodeLog[]>([])
  const listenWebsocket = ref<boolean>(true)

  const nodeProviders = ref<Record<string, string[]>>({})
  // state
  const $jsonRpc = inject<IJsonRpcService>('$jsonRpc')!
  const validators = ref<ValidatorModel[]>([])
  const updateValidatorModalOpen = ref<boolean>(false)
  const createValidatorModalOpen = ref<boolean>(false)
  const deleteValidatorModalOpen = ref<boolean>(false)

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

  const createValidatorModelValid = computed(() => {
    return (
      validatorToCreate.value?.model !== '' &&
      validatorToCreate.value?.provider !== '' &&
      validatorToCreate.value?.stake
    )
  })

  const updateValidatorModelValid = computed(() => {
    return (
      validatorToUpdate.value?.model !== '' &&
      validatorToUpdate.value?.provider !== '' &&
      validatorToUpdate.value?.stake
    )
  })

  const selectedValidator = ref<ValidatorModel>()

  if (!webSocketClient.connected) webSocketClient.connect()
  webSocketClient.on('status_update', (event) => {
    if (listenWebsocket.value) {
      if (event.message?.function !== 'get_transaction_by_id') {
        logs.value.push({ date: new Date().toISOString(), message: event.message })
      }
    }
  })

  function initialize() {
    selectedValidator.value = undefined
    updateValidatorModalOpen.value = false
    createValidatorModalOpen.value = false
    deleteValidatorModalOpen.value = false
    validators.value = []

    validatorToUpdate.value = {
      model: '',
      provider: '',
      stake: 0,
      config: '{ }'
    }
    validatorToCreate.value = {
      model: '',
      provider: '',
      stake: 0,
      config: '{ }'
    }
  }

  async function getValidatorsData() {
    const [validatorsResult, modelsResult] = await Promise.all([
      $jsonRpc.getValidators(),
      $jsonRpc.getProvidersAndModels()
    ])

    if (validatorsResult?.status === 'success') {
      validators.value = validatorsResult.data
    } else {
      throw new Error('Error getting validators')
    }

    if (modelsResult?.status === 'success') {
      nodeProviders.value = modelsResult.data
    } else {
      throw new Error('Error getting Providers and Models data')
    }
  }

  function openDeleteValidatorModal(validator: ValidatorModel) {
    selectedValidator.value = validator
    deleteValidatorModalOpen.value = true
  }

  function openUpdateValidatorModal(validator: ValidatorModel) {
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

  function closeUpdateValidatorModal() {
    selectedValidator.value = undefined
    updateValidatorModalOpen.value = false
    validatorToUpdate.value = {
      model: '',
      provider: '',
      stake: 0,
      config: '{ }'
    }
  }

  function closeDeleteValidatorModal() {
    selectedValidator.value = undefined
    deleteValidatorModalOpen.value = false
  }

  async function updateValidator() {
    const { stake, provider, model, config } = validatorToUpdate.value

    if (stake <= 0 || !provider || !model || !config) {
      throw new Error('Please fill all the required fields')
    }
    const contractConfig = JSON.parse(config || '{}')
    const result = await $jsonRpc.updateValidator({
      address: selectedValidator.value?.address || '',
      stake,
      provider,
      model,
      config: contractConfig
    })
    if (result?.status === 'success') {
      const index = validators.value.findIndex(
        (v) => v.address === selectedValidator.value?.address
      )

      if (index >= 0) {
        validators.value.splice(index, 1, result.data)
      }
      closeUpdateValidatorModal()
    } else {
      throw new Error('Error udpating the validator')
    }
  }

  const deleteValidator = async () => {
    const address = selectedValidator.value?.address
    if (validators.value.length === 1) {
      throw new Error('You must have at least one validator')
    }
    const result = await $jsonRpc.deleteValidator({
      address: address || ''
    })
    if (result?.status === 'success') {
      validators.value = validators.value.filter((v) => v.address !== address)
    } else {
      throw new Error('Error deleting the validator')
    }

    closeDeleteValidatorModal()
  }

  function openCreateNewValidatorModal() {
    createValidatorModalOpen.value = true
  }

  function closeNewValidatorModal() {
    createValidatorModalOpen.value = false
    validatorToCreate.value = {
      model: '',
      provider: '',
      stake: 0,
      config: '{ }'
    }
  }

  async function createNewValidator() {
    if (!validatorToCreate.value.stake) {
      throw new Error('Please fill the stake field')
    }
    const { stake, provider, model, config } = validatorToCreate.value
    const result = await $jsonRpc.createValidator({ stake, provider, model, config })
    if (result?.status === 'success') {
      validators.value.push(result.data)
      closeNewValidatorModal()
    } else {
      throw new Error('Error creating a new validator')
    }
  }
  return {
    logs,
    listenWebsocket,
    validators,
    nodeProviders,
    updateValidatorModalOpen,
    createValidatorModalOpen,
    deleteValidatorModalOpen,
    selectedValidator,
    validatorToUpdate,
    validatorToCreate,
    updateValidatorModelValid,
    createValidatorModelValid,

    initialize,
    getValidatorsData,
    createNewValidator,
    deleteValidator,
    updateValidator,
    openUpdateValidatorModal,
    closeUpdateValidatorModal,
    openDeleteValidatorModal,
    closeDeleteValidatorModal,
    closeNewValidatorModal,
    openCreateNewValidatorModal
  }
})
