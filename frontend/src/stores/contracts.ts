import type { IJsonRpcService } from '@/services'
import type { ContractFile, DeployedContract } from '@/types'
import { getContractFileName } from '@/utils'
import { defineStore } from 'pinia'
import { ref, inject } from 'vue'

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
    setCurrentContractId
  }
})
