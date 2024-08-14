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
}

export interface NewValidatorDataModel {
  config: string;
  model: string;
  provider: string;
  stake: number;
}

export interface ContractMethod {
  name: string;
  inputs: { [k: string]: string };
}

export type Address = `0x${string}`;
