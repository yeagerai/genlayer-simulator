import type { JsonRPCRequest, JsonRPCResponse, JsonRPCResult } from "@/types"

  export interface IJsonRPCService {
    call({ method, params }: JsonRPCRequest) : Promise<JsonRPCResponse<any>>;
    getContractState(request: { contractAddress: string, method: string, methodArguments: any[]}) : Promise<JsonRPCResult>;
    callContractFunction(request: { userAccount: string, contractAddress: string, method: string, params: any[]}) : Promise<JsonRPCResult>;
    deployContract(request: { userAccount: string, className: string, code: string, constructorParams: string}) : Promise<JsonRPCResult>;
    getContractSchema(request: { code: string}) : Promise<JsonRPCResult>;
    getDeployedContractSchema(request: { address: string}) : Promise<JsonRPCResult>;
    getValidators() : Promise<JsonRPCResult>;
    getProvidersAndModels() : Promise<JsonRPCResult>;
    createValidator(request: { stake: number, provider: string, model: string, config: any }) : Promise<JsonRPCResult>;
    updateValidator(request: { address: string, stake: number, provider: string, model: string, config: any }) : Promise<JsonRPCResult>;
    deleteValidator(request: { address: string }) : Promise<JsonRPCResult>;
  }
