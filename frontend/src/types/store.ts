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
  scope: string;
  name: string;
  type: 'error' | 'warning' | 'info' | 'success';
  message: string;
  data: any;
  // message: {
  //   function: string;
  //   trace_id: string;
  //   response: {
  //     status: string;
  //     message: string;
  //     data?: any;
  //   };
  // };
  // mock?: boolean;
}

// export interface RPCLog extends NodeLog {
//   data: {
//     function: string;
//     trace_id: string;
//     response: {
//       status: string;
//       message: string;
//       data?: any;
//     };
//   };
// }

export interface RPCResponseEventData {
  function_name: string;
  trace_id: string;
  response: {
    status: 'error' | 'warning' | 'info' | 'success';
    message: string;
    data?: any;
  };
}

export interface TransactionStatusUpdateEventData {
  hash: string;
  new_status: string;
}

export interface TransactionItem {
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
