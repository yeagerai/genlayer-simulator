import type { IJsonRpcService } from '@/services'
import type { ContractFile, DeployedContract } from '@/types'
import { getContractFileName } from '@/utils'
import { defineStore } from 'pinia'
import { ref, inject } from 'vue'
import { v4 as uuidv4 } from 'uuid'

const getInitialOPenedFiles = (): string[] => {
  const storage = localStorage.getItem('contracts.openedFiles')
  if (storage) return storage.split(',')
  return []
}

export const useContractsStore = defineStore('contractsStore', () => {
  const $jsonRpc = inject<IJsonRpcService>('$jsonRpc') // TODO: will be used in actions

  const contractsModified = ref<string>(localStorage.getItem('contracts.contractsModified') || '')
  const contracts = ref<ContractFile[]>([])
  const openedFiles = ref<string[]>(getInitialOPenedFiles())

  const currentContractId = ref<string | undefined>(
    localStorage.getItem('contracts.currentContractId') || ''
  )
  const deployedContracts = ref<DeployedContract[]>([])
  const transactions = ref<Record<string, any[]>>({})
  const callingContractMethod = ref<boolean>(false)
  const callingContractState = ref<boolean>(false)
  const currentContractState = ref<Record<string, any>>({})
  function addContractFile(contract: ContractFile): void {
    const name = getContractFileName(contract.name)
    contracts.value.push({ ...contract, name })
  }

  function removeContractFile(id: string): void {
    contracts.value = [...contracts.value.filter((c) => c.id !== id)]
    deployedContracts.value = [...deployedContracts.value.filter((c) => c.contractId !== id)]
  }

  function updateContractFile(id: string, { name, content }: { name?: string; content?: string }) {
    contracts.value = [
      ...contracts.value.map((c) => {
        if (c.id === id) {
          const _name = getContractFileName(name || c.name)
          const _content = content || c.content
          return { ...c, name: _name, content: _content }
        }
        return c
      })
    ]
  }

  function openFile(id: string) {
    const index = contracts.value.findIndex((c) => c.id === id)
    const openedIndex = openedFiles.value.findIndex((c) => c === id)

    if (index > -1 && openedIndex === -1) {
      openedFiles.value = [...openedFiles.value, id]
    }
    currentContractId.value = id
  }

  function closeFile(id: string) {
    openedFiles.value = [...openedFiles.value.filter((c) => c !== id)]
    if (openedFiles.value.length > 0) {
      currentContractId.value = openedFiles.value[openedFiles.value.length - 1]
    } else {
      currentContractId.value = undefined
    }
  }

  function addDeployedContract({ contractId, address, defaultState }: DeployedContract): void {
    const index = deployedContracts.value.findIndex((c) => c.contractId === contractId)
    if (index === -1) deployedContracts.value.push({ contractId, address, defaultState })
    else deployedContracts.value[index] = { contractId, address, defaultState }
  }

  function removeDeployedContract(contractId: string): void {
    deployedContracts.value = [
      ...deployedContracts.value.filter((c) => c.contractId !== contractId)
    ]
  }

  function setCurrentContractId(id?: string) {
    currentContractId.value = id || ''
  }

  async function callContractMethod({
    userAccount,
    contractAddress,
    method,
    params
  }: {
    userAccount: string
    contractAddress: string
    method: string
    params: any[]
  }) {
    callingContractMethod.value = true
    try {
      const result = await $jsonRpc?.callContractFunction({
        userAccount,
        contractAddress,
        method,
        params
      })

      callingContractMethod.value = false
      if (result?.status === 'success') {
        if (!transactions.value[contractAddress]) {
          transactions.value[contractAddress] = []
        }

        return result
      }
      return null
    } catch (error) {
      console.error(error)
      callingContractMethod.value = false
      return null
    }
  }

  async function getContractState(
    contractAddress: string,
    method: string,
    methodArguments: string[]
  ) {
    callingContractState.value = true
    try {
      const result = await $jsonRpc?.getContractState({ contractAddress, method, methodArguments })

      currentContractState.value = {
        ...currentContractState.value,
        [method]: result?.data[method]
      }
      callingContractState.value = false
    } catch (error) {
      console.error(error)
      callingContractState.value = false
      return null
    }
  }

  return {
    // state
    contractsModified,
    contracts,
    openedFiles,
    currentContractId,
    deployedContracts,
    transactions,

    //actions
    addContractFile,
    removeContractFile,
    updateContractFile,
    openFile,
    closeFile,
    addDeployedContract,
    removeDeployedContract,
    setCurrentContractId,

    callContractMethod,
    getContractState
  }
})
