export interface ContractFile {
  id: string
  name: string
  content: string
  example?: boolean
}

export interface OpenedFile {
  id: string
  name: string
}

export interface DeployedContract {
  contractId: string
  address: string
  defaultState: string
}

export interface MainStoreState {
  contracts: ContractFile[]
  openedFiles: string[]
  currentContractId?: string
  deployedContracts: DeployedContract[]
  currentUserAddress?: string
  nodeLogs: {
    date: string
    message: {
      function: string
      trace_id: string
      response: {
        status: string
        message: string
        data: any
      }
    }
  }[]
  accounts: string[]
  contractTransactions: Record<string, any>
}

export type UIMode = 'light' | 'dark'
export interface UIState {
  mode: UIMode
  showTutorial: boolean
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
  config: string
  model: string
  provider: string
  stake: number
}

export interface UpdateValidatorModel {
  config: string
  model: string
  provider: string
  stake: number
}

export interface ContractMethod {
  name: string
  inputs: { [k: string]: string }
}

export interface JsonRPCRequest {
  method: string
  params: any[]
}

export interface JsonRPCResponse {
  id: string
  jsonrpc: string
  result: {
    data: any
    message: string
    status: string
  }
}
