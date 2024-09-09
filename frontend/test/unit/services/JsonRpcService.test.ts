import { JsonRpcService } from '@/services/JsonRpcService';
import type { IJsonRpcService } from '@/services/IJsonRpcService';
import type { IRpcClient } from '@/clients/rpc';
import type { GetContractStateResult, JsonRPCResponse } from '@/types';
import { describe, expect, it, vi, afterEach, beforeEach } from 'vitest';

describe('JsonRprService', () => {
  let jsonRpcService: IJsonRpcService;
  const rpcClient: IRpcClient = vi.fn();
  beforeEach(() => {
    jsonRpcService = new JsonRpcService(rpcClient);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getContractState', () => {
    const mockResponse: JsonRPCResponse<GetContractStateResult> = {
      id: 'test',
      jsonrpc: '2.0',
      result: {
        data: {
          get_have_coin: 'True',
          id: '0x58FaA28cbAA1b52F8Ec8D3c6FFCE6f1AaF8bEEB1',
        },
        message: '',
        status: 'success',
      },
    };
    const input = {
      contractAddress: '0x58FaA28cbAA1b52F8Ec8D3c6FFCE6f1AaF8bEEB1',
      userAccount: '0xFEaedeC4c6549236EaF49C1F7c5cf860FD2C3fcB',
      data: '0x',
    };
    it('should call rpc client', async () => {
      const spy = vi
        .spyOn(rpcClient, 'call')
        .mockImplementationOnce(() => Promise.resolve(mockResponse));

      await jsonRpcService.getContractState(input);
      expect(spy.getMockName()).toEqual('call');
      expect(rpcClient.call).toHaveBeenCalledTimes(1);
      expect(rpcClient.call).toHaveBeenCalledWith({
        method: 'call',
        params: [input.contractAddress, input.userAccount, input.data],
      });
    });

    it('should return contract state', async () => {
      vi.spyOn(rpcClient, 'call').mockImplementationOnce(() =>
        Promise.resolve(mockResponse),
      );
      const result = await jsonRpcService.getContractState(input);
      expect(result).to.deep.equal(mockResponse.result);
    });
  });
});
