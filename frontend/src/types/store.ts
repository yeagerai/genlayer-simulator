export interface ContractFile {
  id: string;
  name: string;
  content: string;
  example?: boolean;
  updatedAt?: string;
}

export interface OpenedFile {
  id: string;
  name: string;
}

export interface DeployedContract {
  contractId: string;
  address: string;
  defaultState: string;
}

export interface NodeLog {
  date: string;
  message: {
    function: string;
    trace_id: string;
    response: {
      status: string;
      message: string;
      data?: any;
    };
  };
  mock?: boolean;
}

// TODO: review this
export interface TransactionItem {
  id?: number;
  hash: string;
  type: 'deploy' | 'method';
  status: string;
  contractAddress: string;
  localContractId: string;
  data?: any;
}

export type UIMode = 'light' | 'dark';
export interface UIState {
  mode: UIMode;
  showTutorial: boolean;
}
