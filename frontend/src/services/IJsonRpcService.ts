import type {
  GetContractStateRequest,
  GetContractStateResult,
  DeployContractRequest,
  GetDeployedContractSchemaRequest,
  CreateValidatorRequest,
  UpdateValidatorRequest,
  DeleteValidatorRequest,
  GetContractSchemaRequest,
} from '@/types';

export interface IJsonRpcService {
  getContractState(
    request: GetContractStateRequest,
  ): Promise<GetContractStateResult>;
  sendTransaction(singedTransaction: string): Promise<number>;
  deployContract(request: DeployContractRequest): Promise<number>;
  getContractSchema(request: GetContractSchemaRequest): Promise<any>;
  getDeployedContractSchema(
    request: GetDeployedContractSchemaRequest,
  ): Promise<any>;
  getValidators(): Promise<any[]>;
  getProvidersAndModels(): Promise<any[]>;
  createValidator(request: CreateValidatorRequest): Promise<any>;
  updateValidator(request: UpdateValidatorRequest): Promise<any>;
  deleteValidator(request: DeleteValidatorRequest): Promise<any>;
  getTransactionById(txId: number): Promise<any>;
}
