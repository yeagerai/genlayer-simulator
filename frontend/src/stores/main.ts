import { defineStore } from 'pinia'
import type { ContractFile, MainStoreState, DeployedContract } from '@/types'
import { RpcClient, db, getContractFileName, setupStores } from '@/utils'

const rpcClient = new RpcClient()
const getInitialOPenedFiles = (): string[] => {
  const storage = localStorage.getItem('mainStore.openedFiles')
  if (storage) return storage.split(',')
  return []
}

export const useMainStore = defineStore('mainStore', {
  state: (): MainStoreState => {
    return {
      contracts: [],
      openedFiles: getInitialOPenedFiles(),
      currentContractId: localStorage.getItem('mainStore.currentContractId') || '',
      deployedContracts: [],
      currentUserAddress: localStorage.getItem('mainStore.currentUserAddress') || '',
      nodeLogs: [],
      accounts: localStorage.getItem('mainStore.accounts')
        ? (localStorage.getItem('mainStore.accounts') || '').split(',')
        : [],
      contractTransactions: {}
    }
  },
  actions: {
    addContractFile(contract: ContractFile): void {
      const name = getContractFileName(contract.name)
      this.contracts.push({ ...contract, name })
    },
    removeContractFile(id: string): void {
      this.contracts = [...this.contracts.filter((c) => c.id !== id)]
      this.deployedContracts = [...this.deployedContracts.filter((c) => c.contractId !== id)]
    },
    updateContractFile(id: string, { name, content }: { name?: string; content?: string }) {
      this.contracts = [
        ...this.contracts.map((c) => {
          if (c.id === id) {
            const _name = getContractFileName(name || c.name)
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
      }
      this.currentContractId = id
    },
    closeFile(id: string) {
      this.openedFiles = [...this.openedFiles.filter((c) => c !== id)]
      if (this.openedFiles.length > 0) {
        this.currentContractId = this.openedFiles[this.openedFiles.length - 1]
      } else {
        this.currentContractId = undefined
      }
    },
    addDeployedContract({ contractId, address, defaultState }: DeployedContract): void {
      const index = this.deployedContracts.findIndex((c) => c.contractId === contractId)
      if (index === -1)
        this.$patch((state) => state.deployedContracts.push({ contractId, address, defaultState }))
      else
        this.$patch(
          (state) => (state.deployedContracts[index] = { contractId, address, defaultState })
        )
    },
    removeDeployedContract(contractId: string): void {
      this.deployedContracts = [
        ...this.deployedContracts.filter((c) => c.contractId !== contractId)
      ]
    },
    setCurrentContractId(id?: string) {
      this.currentContractId = id
    },
    async generateNewAccount(): Promise<string | null> {
      try {
        const { result } = await rpcClient.call<any>({
          method: 'create_account',
          params: []
        })
        if (result && result.status === 'success') {
          this.accounts = [...this.accounts, result.data.address]
          this.currentUserAddress = result.data.address
          return result.data.address
        }
        return null
      } catch (error) {
        console.error
        return null
      }
    },
    async resetStorage(): Promise<void> {
      try {
        const contracts = await db.contractFiles.toArray()
        const idsToDelete = contracts.filter((c) => !c.example && !c.updatedAt).map((c) => c.id)

        await db.deployedContracts.where('contractId').anyOf(idsToDelete).delete()
        await db.contractFiles.where('id').anyOf(idsToDelete).delete()

        this.deployedContracts = [
          ...this.deployedContracts.filter((c) => !idsToDelete.includes(c.contractId))
        ]
        this.contracts = [...this.contracts.filter((c) => !idsToDelete.includes(c.id))]
        this.openedFiles = [...this.openedFiles.filter((c) => !idsToDelete.includes(c))]
        if (this.currentContractId && idsToDelete.includes(this.currentContractId)) {
          this.currentContractId = ''
        }

        localStorage.setItem('mainStore.currentContractId', this.currentContractId || '')
        localStorage.setItem('mainStore.openedFiles', this.openedFiles.join(','))

        await setupStores()
      } catch (error) {
        console.error(error)
      }
    }
  }
})
