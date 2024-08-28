import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useRpcClient } from '@/hooks';
import { RpcClient } from '@/clients/rpc';
import { JsonRpcService } from '@/services/JsonRpcService';

// Mock RpcClient and JsonRpcService
vi.mock('@/clients/rpc', () => ({
  RpcClient: vi.fn(),
}));

vi.mock('@/services/JsonRpcService', () => ({
  JsonRpcService: vi.fn(),
}));

describe('useRpcClient', () => {
  beforeEach(() => {
    vi.clearAllMocks(); // Clear mock calls between tests
  });

  it('should create a new JsonRpcService with a new RpcClient instance', () => {
    useRpcClient();

    // Verify that RpcClient is called once
    expect(RpcClient).toHaveBeenCalledTimes(1);

    // Verify that JsonRpcService is called with a new RpcClient instance
    expect(JsonRpcService).toHaveBeenCalledWith(expect.any(RpcClient));
    expect(JsonRpcService).toHaveBeenCalledTimes(1);
  });
});
