const JSON_RPC_SERVER_URL = import.meta.env.VITE_JSON_RPC_SERVER_URL;
import type { JsonRPCRequest, JsonRPCResponse } from '@/types';
import { v4 as uuidv4 } from 'uuid';

export interface IRpcClient {
  call<T>(request: JsonRPCRequest): Promise<JsonRPCResponse<T>>;
}

export class RpcClient implements IRpcClient {
  async call<T>({
    method,
    params,
  }: JsonRPCRequest): Promise<JsonRPCResponse<T>> {
    const requestId = uuidv4();
    const data = {
      jsonrpc: '2.0',
      method,
      params,
      id: requestId,
    };
    const response = await fetch(JSON_RPC_SERVER_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return response.json() as Promise<JsonRPCResponse<T>>;
  }
}
