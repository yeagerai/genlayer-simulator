import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useRpcClient } from '@/hooks';
import { RpcClient } from '@/clients/rpc';
import { JsonRpcService } from '@/services/JsonRpcService';

vi.mock('@/clients/rpc', () => ({
  RpcClient: vi.fn(),
}));

vi.mock('@/services/JsonRpcService', () => ({
  JsonRpcService: vi.fn(),
}));

describe('useRpcClient', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should create a new JsonRpcService with a new RpcClient instance', () => {
    useRpcClient();

    expect(RpcClient).toHaveBeenCalledTimes(1);
    expect(JsonRpcService).toHaveBeenCalledWith(expect.any(RpcClient));
    expect(JsonRpcService).toHaveBeenCalledTimes(1);
  });
});
