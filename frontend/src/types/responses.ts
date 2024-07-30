import type { JsonRpcResult } from './results';

export interface JsonRPCResponse<T> {
  id: string;
  jsonrpc: string;
  result: JsonRpcResult<T>;
}
