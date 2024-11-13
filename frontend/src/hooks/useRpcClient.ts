import { RpcClient } from '@/clients/rpc';
import { JsonRpcService } from '@/services/JsonRpcService';

export function useRpcClient() {
  return new JsonRpcService(new RpcClient());
}
