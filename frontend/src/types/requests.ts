export interface JsonRPCRequest {
  method: string;
  params: any[];
}

export interface GetContractStateRequest {
  contractAddress: string;
  userAccount: string;
  data: string;
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
  config?: Record<string, any>;
  plugin?: string;
  plugin_config?: Record<string, any>;
}

export interface UpdateValidatorRequest {
  address: string;
  stake: number;
  provider: string;
  model: string;
  config?: Record<string, any>;
  plugin?: string;
  plugin_config?: Record<string, any>;
}

export interface DeleteValidatorRequest {
  address: string;
}

export interface AddProviderRequest {
  provider: string;
  model: string;
  config: Record<string, any>;
  plugin: string;
  plugin_config: Record<string, any>;
}

export interface UpdateProviderRequest {
  id: number;
  provider: string;
  model: string;
  config: Record<string, any>;
  plugin: string;
  plugin_config: Record<string, any>;
}

export interface DeleteProviderRequest {
  id: number;
}
