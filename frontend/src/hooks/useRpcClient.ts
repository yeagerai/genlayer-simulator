import { RpcClient } from '@/clients/rpc';
import { JsonRpcService } from '@/services/JsonRpcService';

// TODO: should this be 100% replaced with useGenlayer?

export function useRpcClient() {
  return new JsonRpcService(new RpcClient());
}
