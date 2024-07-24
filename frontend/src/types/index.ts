export * from './results';
export * from './requests';
export * from './responses';
export * from './store';

export interface ValidatorModel {
  address: string;
  config: any;
  id: number;
  model: string;
  provider: string;
  stake: number;
  updated_at: string;
}

export interface CreateValidatorModel {
  config: string;
  model: string;
  provider: string;
  stake: number;
}

export interface UpdateValidatorModel {
  config: string;
  model: string;
  provider: string;
  stake: number;
}

export interface ContractMethod {
  name: string;
  inputs: { [k: string]: string };
}
