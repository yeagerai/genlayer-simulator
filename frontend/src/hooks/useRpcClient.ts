import { RpcClient } from '@/utils';
import { JsonRpcService } from '@/services/JsonRpcService';

export function useRpcClient() {
  return new JsonRpcService(new RpcClient());
}
