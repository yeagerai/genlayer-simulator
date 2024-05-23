import { rpcClient } from "@/utils";
import type { IJsonRPCService } from "./IJsonRpcService";
import type { JsonRPCRequest, JsonRPCResponse, } from "@/types";
import { JsonRPCResult } from "../types";

export class JsonRprService implements IJsonRPCService {
    getContractState(request: { contractAddress: string; method: string; methodArguments: any[]; }): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    callContractFunction(request: { userAccount: string; contractAddress: string; method: string; params: any[]; }): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    deployContract(request: { userAccount: string; className: string; code: string; constructorParams: string; }): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    getContractSchema(request: { code: string; }): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    getDeployedContractSchema(request: { address: string; }): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    getValidators(): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    getProvidersAndModels(): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    createValidator(request: { stake: number; provider: string; model: string; config: any; }): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    updateValidator(request: { address: string; stake: number; provider: string; model: string; config: any; }): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    deleteValidator(request: { address: string; }): Promise<JsonRPCResult> {
        throw new Error("Method not implemented.");
    }
    call({ method, params }: JsonRPCRequest) : Promise<JsonRPCResponse> {
        return rpcClient.call({ method, params })
    }
}





// method: 'get_contract_state',
// params: [contractAddress, method, methodArguments]


// method: 'call_contract_function',
// params: [
//   store.currentUserAddress,
//   deployedContract.value?.address,
//   `${abi.value.class}.${method}`,
//   params
// ]


// method: 'deploy_intelligent_contract',
// params: [
//   store.currentUserAddress,
//   contractSchema.class,
//   contract.content,
//   constructorParamsAsString
// ]


// const { result } = await $jsonRpc.call({
//   method: 'get_icontract_schema',
//   params: [contract.address]
// })


// const { result } = await $jsonRpc.call({
//   method: 'get_icontract_schema_for_code',
//   params: [contract.value.content]
// })

// method: 'get_all_validators',
// params: []


// method: 'get_providers_and_models',
// params: []


// const { result } = await $jsonRpc.call({
//   method: 'update_validator',
//   params: [selectedValidator.value?.address, stake, provider, model, contractConfig]
// })

// const { result } = await $jsonRpc.call({
//   method: 'delete_validator',
//   params: [address]
// })

// const { result } = await $jsonRpc.call({
//   method: 'create_validator',
//   params: [stake, provider, model, config]
// })