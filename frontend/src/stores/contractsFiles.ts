import { defineStore } from 'pinia'
import type { ContractFile, ContractsState, DefaultContractState, DeployedContract } from '@/types'

const getInitialOPenedFiles = (): string[] => {
  const storage = localStorage.getItem('contractFiles.openedFiles')
  if (storage) return storage.split(',')
  return []
}

export const useContractsFilesStore = defineStore('contractsFiles', {
  state: (): ContractsState => {
    return {
      contracts: [],
      openedFiles: getInitialOPenedFiles(),
      currentContractId: localStorage.getItem('contractFiles.currentContractId') || '',
      deployedContracts: [],
      defaultContractStates: []
    }
  },
  actions: {
    addContractFile(contract: ContractFile): void {
      this.contracts.push(contract)
    },
    removeContractFile(id: string): void {
      this.contracts = [...this.contracts.filter((c) => c.id !== id)]
      this.deployedContracts = [...this.deployedContracts.filter((c) => c.contractId !== id)]
      this.defaultContractStates = [
        ...this.defaultContractStates.filter((c) => c.contractId !== id)
      ]
    },
    updateContractFile(id: string, { name, content }: { name?: string; content?: string }) {
      this.contracts = [
        ...this.contracts.map((c) => {
          if (c.id === id) {
            const _name = name || c.name
            const _content = content || c.content
            return { ...c, name: _name, content: _content }
          }
          return c
        })
      ]
    },
    openFile(id: string) {
      const index = this.contracts.findIndex((c) => c.id === id)
      const openedIndex = this.openedFiles.findIndex((c) => c === id)

      if (index > -1 && openedIndex === -1) {
        this.openedFiles = [...this.openedFiles, id]
        this.currentContractId = id
      }
    },
    closeFile(id: string) {
      this.openedFiles = [...this.openedFiles.filter((c) => c !== id)]
      if (this.openedFiles.length > 0) {
        this.currentContractId = this.openedFiles[this.openedFiles.length - 1]
      } else {
        this.currentContractId = undefined
      }
    },
    addDeployedContract({ contractId, address }: DeployedContract): void {
      const index = this.deployedContracts.findIndex((c) => c.contractId === contractId)
      if (index === -1)
        this.$patch((state) => state.deployedContracts.push({ contractId, address }))
      else this.$patch((state) => (state.deployedContracts[index] = { contractId, address }))
    },
    addDefaultContractState({ contractId, address, defaultState }: DefaultContractState): void {
      const index = this.defaultContractStates.findIndex((c) => c.contractId === contractId)
      if (index === -1)
        this.$patch((state) =>
          state.defaultContractStates.push({ contractId, address, defaultState })
        )
      else
        this.$patch(
          (state) => (state.defaultContractStates[index] = { contractId, address, defaultState })
        )
    },
    setCurrentContractId(id?: string) {
      this.currentContractId = id
    }
  }
})
