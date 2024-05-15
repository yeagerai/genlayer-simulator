import { rpcClient } from "@/utils";
import type { IJsonRPCService } from "./IJsonRpcService";
import type { JsonRPCRequest, JsonRPCResponse } from "@/types";

export class JsonRprService implements IJsonRPCService {
    call({ method, params }: JsonRPCRequest) : Promise<JsonRPCResponse> {
        return rpcClient.call({ method, params })
    }
}