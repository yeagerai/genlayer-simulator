export * from './results';
export * from './requests';
export * from './responses';
export * from './store';
export * from './events';

export interface ValidatorModel {
  address: string;
  config: any;
  id: number;
  model: string;
  provider: string;
  stake: number;
  updated_at: string;
  plugin: string;
  plugin_config: Record<string, any>;
}

export interface NewValidatorDataModel {
  config: string;
  model: string;
  provider: string;
  stake: number;
}

export interface ProviderModel {
  id: number;
  provider: string;
  model: string;
  config: Record<string, any>;
  plugin: string;
  plugin_config: Record<string, any>;
  is_available: boolean;
  is_model_available: boolean;
}

export interface NewProviderDataModel {
  provider: string;
  model: string;
  // config: Record<string, any>;
  config: string;
  plugin: string;
  plugin_config: string;
  // plugin_config: Record<string, any>;
  // api_key_env_var: string;
  // api_url: string | null;
}

export interface ContractMethod {
  type: string;
  name: string;
  inputs: [{ name: string; type: string }];
  outputs: [{ name: string; type: string }];
}

export type Address = `0x${string}`;
