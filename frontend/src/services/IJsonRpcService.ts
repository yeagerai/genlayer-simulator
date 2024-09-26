import type {
  GetContractStateRequest,
  GetContractStateResult,
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
  sendTransaction(signedTransaction: string): Promise<string>;
  getContractSchema(request: GetContractSchemaRequest): Promise<any>;
  getDeployedContractSchema(
    request: GetDeployedContractSchemaRequest,
  ): Promise<any>;
  getValidators(): Promise<any[]>;
  getProvidersAndModels(): Promise<any[]>;
  createValidator(request: CreateValidatorRequest): Promise<any>;
  updateValidator(request: UpdateValidatorRequest): Promise<any>;
  deleteValidator(request: DeleteValidatorRequest): Promise<any>;
  getTransactionByHash(hash: string): Promise<any>;
}
