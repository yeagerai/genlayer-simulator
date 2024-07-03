import type {
  GetContractStateRequest,
  JsonRPCRequest,
  JsonRPCResponse,
  JsonRpcResult,
  GetContractStateResult,
  CallContractFunctionResult,
  CallContractFunctionRequest,
  DeployContractRequest,
  GetDeployedContractSchemaRequest,
  CreateValidatorRequest,
  UpdateValidatorRequest,
  DeleteValidatorRequest,
  GetContractSchemaRequest
} from '@/types'

export interface IJsonRpcService {
  call(request: JsonRPCRequest): Promise<JsonRPCResponse<any>>
  getContractState(request: GetContractStateRequest): Promise<JsonRpcResult<GetContractStateResult>>
  callContractFunction(
    request: CallContractFunctionRequest
  ): Promise<JsonRpcResult<CallContractFunctionResult>>
  deployContract(request: DeployContractRequest): Promise<JsonRpcResult<any>>
  getContractSchema(request: GetContractSchemaRequest): Promise<JsonRpcResult<any>>
  getDeployedContractSchema(request: GetDeployedContractSchemaRequest): Promise<JsonRpcResult<any>>
  getValidators(): Promise<JsonRpcResult<any>>
  getProvidersAndModels(): Promise<JsonRpcResult<any>>
  createValidator(request: CreateValidatorRequest): Promise<JsonRpcResult<any>>
  updateValidator(request: UpdateValidatorRequest): Promise<JsonRpcResult<any>>
  deleteValidator(request: DeleteValidatorRequest): Promise<JsonRpcResult<any>>
  createAccount(): Promise<JsonRpcResult<any>>
  getTransactionById(txId: number): Promise<JsonRpcResult<any>>
}
