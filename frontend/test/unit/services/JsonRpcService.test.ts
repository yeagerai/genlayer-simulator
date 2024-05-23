import { beforeEach, describe, afterEach, it } from 'node:test'
import { expect } from 'chai'
import * as sinon from 'sinon';
import { JsonRprService } from '../../../src/services/JsonRpcService';
import { rpcClient } from '../../../src/utils';
import { JsonRPCResult } from '../../../src/types';

describe('JsonRprService', () => {
  let jsonRpcService: JsonRprService;

  beforeEach(() => {
    jsonRpcService = new JsonRprService();
  });

  afterEach(() => {
    sinon.restore();
  });

  describe('getContractState', () => {
    it('should get contract state', async () => {
      const mockResult: JsonRPCResult<any> = { result: 'mocked result' };
      sinon.stub(rpcClient, 'call').resolves({ result: mockResult });

      const result = await jsonRpcService.getContractState({
        contractAddress: 'address',
        method: 'method',
        methodArguments: ['arg1', 'arg2'],
      });

      expect(result).to.deep.equal('mocked result');
      sinon.assert.calledOnce(rpcClient.call);
    });
  });

  describe('callContractFunction', () => {
    it('should call contract function and return result', async () => {
      const mockResult: JsonRPCResult<any> = { result: 'mocked result' };
      sinon.stub(rpcClient, 'call').resolves({ result: mockResult });

      const result = await jsonRpcService.callContractFunction({
        userAccount: 'user',
        contractAddress: 'address',
        method: 'method',
        params: [1, 2, 3],
      });

      expect(result).to.deep.equal('mocked result');
      sinon.assert.calledOnce(rpcClient.call);
    });
  });

  // Add similar test cases for other methods

});
