import type { JsonRPCRequest, JsonRPCResponse, JsonRPCResult } from "@/types"

  export interface IJsonRPCService {
    call({ method, params }: JsonRPCRequest) : Promise<JsonRPCResponse<any>>;
    getContractState(request: { contractAddress: string, method: string, methodArguments: any[]}) : Promise<JsonRPCResult<any>>;
    callContractFunction(request: { userAccount: string, contractAddress: string, method: string, params: any[]}) : Promise<JsonRPCResult<any>>;
    deployContract(request: { userAccount: string, className: string, code: string, constructorParams: string}) : Promise<JsonRPCResult<any>>;
    getContractSchema(request: { code: string}) : Promise<JsonRPCResult<any>>;
    getDeployedContractSchema(request: { address: string}) : Promise<JsonRPCResult<any>>;
    getValidators() : Promise<JsonRPCResult<any>>;
    getProvidersAndModels() : Promise<JsonRPCResult<any>>;
    createValidator(request: { stake: number, provider: string, model: string, config: any }) : Promise<JsonRPCResult<any>>;
    updateValidator(request: { address: string, stake: number, provider: string, model: string, config: any }) : Promise<JsonRPCResult<any>>;
    deleteValidator(request: { address: string }) : Promise<JsonRPCResult<any>>;
  }
