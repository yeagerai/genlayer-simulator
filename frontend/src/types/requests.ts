export interface JsonRPCRequest {
  method: string;
  params: any[];
}

export interface GetContractStateRequest {
  userAccount: string;
  contractAddress: string;
  data: string;
}

export interface CallContractFunctionRequest {
  userAccount: string;
  contractAddress: string;
  method: string;
  params: any[];
}

export interface DeployContractRequest {
  userAccount: string;
  className: string;
  code: string;
  constructorParams: string;
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
