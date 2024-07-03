import type { IJsonRpcService } from '@/services'
import type { ContractFile, DeployedContract, TransactionItem } from '@/types'
import { getContractFileName } from '@/utils'
import { defineStore } from 'pinia'
import { ref, inject, computed } from 'vue'
import { useAccountsStore } from './accounts'
import { useTransactionsStore } from './transactions'
const getInitialOPenedFiles = (): string[] => {
  const storage = localStorage.getItem('contractsStore.openedFiles')
  if (storage) return storage.split(',')
  return []
}

export const useContractsStore = defineStore('contractsStore', () => {
  const $jsonRpc = inject<IJsonRpcService>('$jsonRpc') // TODO: will be used in actions
  const accountsStore = useAccountsStore()
  const transactionsStore = useTransactionsStore()
  const contracts = ref<ContractFile[]>([])
  const openedFiles = ref<string[]>(getInitialOPenedFiles())

  const currentContractId = ref<string | undefined>(
    localStorage.getItem('contractsStore.currentContractId') || ''
  )
  const deployedContracts = ref<DeployedContract[]>([])
  const callingContractMethod = ref<boolean>(false)
  const callingContractState = ref<boolean>(false)
  const currentContractState = ref<Record<string, any>>({})

  const currentConstructorInputs = ref<{ [k: string]: string }>({})
  const currentErrorConstructorInputs = ref<Error>()
  const currentDeployedContractAbi = ref<any>()

  const loadingConstructorInputs = ref(false)
  const deployingContract = ref(false)

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
    const newItem = { contractId, address, defaultState }
    if (index === -1) deployedContracts.value.push(newItem)
    else deployedContracts.value = deployedContracts.value.splice(index, 1, newItem)
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
    localContractId,
    method,
    params
  }: {
    userAccount: string
    localContractId: string
    method: string
    params: any[]
  }) {
    callingContractMethod.value = true
    try {
      const contract = deployedContracts.value.find((c) => c.contractId === localContractId)
      const result = await $jsonRpc?.callContractFunction({
        userAccount,
        contractAddress: contract?.address || '',
        method,
        params
      })

      callingContractMethod.value = false
      if (result?.status === 'success') {
        transactionsStore.addTransaction({
          contractAddress: contract?.address || '',
          localContractId: contract?.contractId || '',
          txId: (result?.data as any).transaction_id,
          type: 'method',
          status: 'PENDING',
          data: {}
        })

        return true
      }
    } catch (error) {
      console.error(error)
      callingContractMethod.value = false
    }
    return false
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
        [method]: result?.data
      }
      callingContractState.value = false
    } catch (error) {
      console.error(error)
      callingContractState.value = false
      throw new Error('Error getting the contract state')
    }
  }

  async function deployContract({
    constructorParams
  }: {
    constructorParams: { [k: string]: string }
  }) {
    if (currentContract.value) {
      if (
        Object.keys({ ...currentConstructorInputs.value }).length !==
        Object.keys(constructorParams).length
      ) {
        throw new Error('You should provide a valid default state')
      } else {
        // Getting the ABI to check the class name
        let contractSchema = null
        loadingConstructorInputs.value = true
        try {
          const result = await $jsonRpc?.getContractSchema({
            code: currentContract.value.content
          })

          contractSchema = result?.data
          loadingConstructorInputs.value = false
          currentErrorConstructorInputs.value = undefined
        } catch (error) {
          console.error(error)
          loadingConstructorInputs.value = false
          currentErrorConstructorInputs.value = error as Error

          throw new Error('Error getting the contract schema')
        }

        if (contractSchema) {
          // Deploy the contract
          deployingContract.value = true
          try {
            const constructorParamsAsString = JSON.stringify(constructorParams)
            const result = await $jsonRpc?.deployContract({
              userAccount: accountsStore.currentUserAddress || '',
              className: contractSchema.class,
              code: currentContract.value.content,
              constructorParams: constructorParamsAsString
            })
            deployingContract.value = false
            if (result?.status === 'success') {
              deployedContracts.value = deployedContracts.value.filter(
                (c) => c.contractId !== currentContract.value?.id
              )
              const tx: TransactionItem = {
                contractAddress: result?.data.contract_address,
                localContractId: currentContract.value.id,
                txId: result?.data.transaction_id,
                type: 'deploy',
                status: 'PENDING',
                data: {}
              }

              transactionsStore.addTransaction(tx)

              return tx
            } else {
              throw new Error(
                typeof result?.message === 'string'
                  ? result.message
                  : 'Error Deploying the contract'
              )
            }
          } catch (error) {
            console.error(error)
            throw new Error('Error Deploying the contract')
          }
        }
      }
    }
  }

  async function getCurrentContractAbi() {
    try {
      const result = await $jsonRpc?.getDeployedContractSchema({
        address: deployedContract.value?.address || ''
      })
      currentDeployedContractAbi.value = result?.data
    } catch (error) {
      console.error(error)
      if (deployedContract.value) {
        removeDeployedContract(deployedContract.value?.contractId || '')
      }
    }
  }

  async function getConstructorInputs() {
    {
      if (currentContract.value) {
        loadingConstructorInputs.value = true
        try {
          const result = await $jsonRpc?.getContractSchema({
            code: currentContract.value.content
          })
          if (!currentConstructorInputs.value) {
            currentConstructorInputs.value = result?.data?.methods['__init__']?.inputs
          } else {
            //compare existing inputs with new ones
            if (
              JSON.stringify(currentConstructorInputs.value) !==
              JSON.stringify(result?.data?.methods['__init__']?.inputs)
            ) {
              currentConstructorInputs.value = result?.data?.methods['__init__']?.inputs
            }
          }
          currentErrorConstructorInputs.value = undefined
        } catch (error) {
          console.error(error)
          currentErrorConstructorInputs.value = error as Error
        } finally {
          loadingConstructorInputs.value = false
        }
      }
    }
  }

  const currentContract = computed(() => {
    return contracts.value.find((c) => c.id === currentContractId.value)
  })
  const deployedContract = computed(() => {
    return deployedContracts.value.find((c) => c.contractId === currentContractId.value)
  })

  return {
    // state
    contracts,
    openedFiles,
    currentContractId,
    deployedContracts,
    currentContractState,
    callingContractState,
    callingContractMethod,
    currentConstructorInputs,
    currentErrorConstructorInputs,
    currentDeployedContractAbi,
    loadingConstructorInputs,
    deployingContract,

    //getters
    deployedContract,
    currentContract,

    //actions
    addContractFile,
    removeContractFile,
    updateContractFile,
    openFile,
    closeFile,
    addDeployedContract,
    removeDeployedContract,
    setCurrentContractId,
    getCurrentContractAbi,
    callContractMethod,
    getContractState,
    deployContract,
    getConstructorInputs
  }
})
