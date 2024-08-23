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

export interface TransactionItem {
  type: 'deploy' | 'method';
  status: string;
  contractAddress: string;
  localContractId: string;
  txId: number;
  data?: any;
}

export type UIMode = 'light' | 'dark';
export interface UIState {
  mode: UIMode;
  showTutorial: boolean;
}
