import type {
  GetContractStateRequest,
  JsonRPCRequest,
  JsonRPCResponse,
  JsonRpcResult,
  GetContractStateResult,
  DeployContractRequest,
  GetDeployedContractSchemaRequest,
  CreateValidatorRequest,
  UpdateValidatorRequest,
  DeleteValidatorRequest,
  GetContractSchemaRequest,
  GetProvidersAndModelsData,
} from '@/types';

export interface IJsonRpcService {
  call(request: JsonRPCRequest): Promise<JsonRPCResponse<any>>;
  getContractState(
    request: GetContractStateRequest,
  ): Promise<JsonRpcResult<GetContractStateResult>>;
  sendTransaction(singedTransaction: string): Promise<JsonRpcResult<any>>;
  deployContract(request: DeployContractRequest): Promise<JsonRpcResult<any>>;
  getContractSchema(
    request: GetContractSchemaRequest,
  ): Promise<JsonRpcResult<any>>;
  getDeployedContractSchema(
    request: GetDeployedContractSchemaRequest,
  ): Promise<JsonRpcResult<any>>;
  getValidators(): Promise<JsonRpcResult<any>>;
  getProvidersAndModels(): Promise<JsonRpcResult<GetProvidersAndModelsData>>;
  createValidator(request: CreateValidatorRequest): Promise<JsonRpcResult<any>>;
  updateValidator(request: UpdateValidatorRequest): Promise<JsonRpcResult<any>>;
  deleteValidator(request: DeleteValidatorRequest): Promise<JsonRpcResult<any>>;
  getTransactionById(txId: number): Promise<JsonRpcResult<any>>;
}
