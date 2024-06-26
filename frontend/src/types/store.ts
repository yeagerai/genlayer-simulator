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
  defaultState: string
}

export interface NodeLog {
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
  mock?: boolean
}

export interface MainStoreState {
  contractsModified: string
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
