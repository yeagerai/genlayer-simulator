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
  type: string;
  name: string;
  inputs: [{ name: string; type: string }];
  outputs: [{ name: string; type: string }];
}

export type Address = `0x${string}`;
