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
export interface DefaultContractState {
  contractId: string
  address: string
  defaultState: string
}

export interface ContractsState {
  contracts: ContractFile[]
  openedFiles: string[]
  currentContractId?: string
  deployedContracts: DeployedContract[]
  defaultContractStates: DefaultContractState[]
}

export type UIMode = 'light' | 'dark'
export interface UIState {
  mode: UIMode
}

export interface ValidatorModel {
  address: string
  config: any
  id: number
  model: string
  provider: string
  stake: number
  updated_at: string
}

export interface CreateValidatorModel {
  stake: number
}

export interface UpdateValidatorModel {
  config: string
  model: string
  provider: string
  stake: number
}
