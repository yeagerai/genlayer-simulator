export interface ContractFile {
  id: string
  name: string
  content: string
}

export interface OpenedFile {
  id: string
  name: string
}

export interface DeployedContract {
  contractId: string
  address: string
}

export interface ContractsState {
  contracts: ContractFile[]
  openedFiles: string[]
  currentContractId?: string
  deployedContracts: DeployedContract[]
}

export type UIMode = 'light' | 'dark'
export interface UIState {
  mode: UIMode
}