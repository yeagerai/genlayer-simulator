export interface JsonRPCRequest {
  method: string;
  params: any[];
}

export interface GetContractStateRequest {
  to: string;
  from: string;
  data: string;
}

export interface GetContractSchemaRequest {
  code: string;
}

export interface GetDeployedContractSchemaRequest {
  address: string;
}

export interface CreateValidatorRequest {
  stake: number;
  provider: string;
  model: string;
  config: any;
}

export interface UpdateValidatorRequest {
  address: string;
  stake: number;
  provider: string;
  model: string;
  config: any;
}

export interface DeleteValidatorRequest {
  address: string;
}

export interface GetTransactionCountRequest {
  address: string;
}
