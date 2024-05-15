import type { JsonRPCRequest, JsonRPCResponse } from "@/types"


  export interface IJsonRPCService {
    call({ method, params }: JsonRPCRequest) : Promise<JsonRPCResponse>;
  }