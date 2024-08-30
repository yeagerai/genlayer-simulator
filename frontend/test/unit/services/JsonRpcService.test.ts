import { JsonRpcService } from '../../../src/services/JsonRpcService';
import { IJsonRpcService } from '../../../src/services/IJsonRpcService';
import { IRpcClient } from '../../../src/clients/rpc';
import {
  CallContractFunctionResult,
  GetContractStateResult,
  JsonRPCResponse,
} from '../../../src/types';
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
      method: 'get_have_coin',
      methodArguments: [],
    };
    it('should call rpc client', async () => {
      const spy = vi
        .spyOn(rpcClient, 'call')
        .mockImplementationOnce(() => Promise.resolve(mockResponse));

      await jsonRpcService.getContractState(input);
      expect(spy.getMockName()).toEqual('call');
      expect(rpcClient.call).toHaveBeenCalledTimes(1);
      expect(rpcClient.call).toHaveBeenCalledWith({
        method: 'get_contract_state',
        params: [input.contractAddress, input.method, []],
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

  describe('callContractFunction', () => {
    const mockResponse: JsonRPCResponse<CallContractFunctionResult> = {
      id: 'test',
      jsonrpc: '2.0',
      result: {
        data: {
          execution_output: {
            consensus_data:
              '{"final":false,"votes":{"0x46CFb7C09EEc0661dfaE35edf9eefb516Be8c9ED":"agree","0x5cceEce5b0DD5Ca98899CC11cAbd2BcbeeAdaBB2":"agree","0xbF2Ea1ac0FC66dbD4C6b0C78B646571c02e0245c":"agree","0xA9e410DcF02ddBdC525DADebEDC865d119479AB8":"agree"},"leader":{"vote":"agree","result":{"args":["test"],"class":"WizardOfCoin","contract_state":"gASVNwAAAAAAAACMCF9fbWFpbl9flIwMV2l6YXJkT2ZDb2lulJOUKYGUfZSMCWhhdmVfY29pbpSMBFRydWWUc2Iu","eq_outputs":{"leader":{"0":"{\\n\\"reasoning\\": \\"I cannot give you the coin because it holds powerful magic that must not fall into the wrong hands.\\",\\n\\"give_coin\\": False\\n}"}},"gas_used":0,"method":"ask_for_coin","mode":"leader","node_config":{"address":"0xB1971EAfB15Fd2a04afAd55A7d5eF9940c0dd464","config":{},"id":1,"model":"gpt-3.5-turbo","provider":"openai","stake":6.9066502309882605,"type":"validator","updated_at":"05/27/2024, 19:50:36"}}},"validators":[{"vote":"agree","result":{"args":["test"],"class":"WizardOfCoin","contract_state":"gASVNwAAAAAAAACMCF9fbWFpbl9flIwMV2l6YXJkT2ZDb2lulJOUKYGUfZSMCWhhdmVfY29pbpSMBFRydWWUc2Iu","eq_outputs":{"leader":{"0":"{\\n\\"reasoning\\": \\"I cannot give you the coin because it holds powerful magic that must not fall into the wrong hands.\\",\\n\\"give_coin\\": False\\n}"}},"gas_used":0,"method":"ask_for_coin","mode":"validator","node_config":{"address":"0x5cceEce5b0DD5Ca98899CC11cAbd2BcbeeAdaBB2","config":{},"id":10,"model":"gpt-4","provider":"openai","stake":8.800945043259368,"type":"validator","updated_at":"05/27/2024, 19:50:36"}}},{"vote":"agree","result":{"args":["test"],"class":"WizardOfCoin","contract_state":"gASVNwAAAAAAAACMCF9fbWFpbl9flIwMV2l6YXJkT2ZDb2lulJOUKYGUfZSMCWhhdmVfY29pbpSMBFRydWWUc2Iu","eq_outputs":{"leader":{"0":"{\\n\\"reasoning\\": \\"I cannot give you the coin because it holds powerful magic that must not fall into the wrong hands.\\",\\n\\"give_coin\\": False\\n}"}},"gas_used":0,"method":"ask_for_coin","mode":"validator","node_config":{"address":"0xbF2Ea1ac0FC66dbD4C6b0C78B646571c02e0245c","config":{"mirostat":0,"mirostat_tau":6.0,"num_gqa":5,"num_thread":14,"repeat_penalty":1.3,"stop":"","tfs_z":1.0,"top_k":31,"top_p":0.96},"id":3,"model":"llama2","provider":"ollama","stake":1.7517946864812701,"type":"validator","updated_at":"05/27/2024, 19:50:36"}}},{"vote":"agree","result":{"args":["test"],"class":"WizardOfCoin","contract_state":"gASVNwAAAAAAAACMCF9fbWFpbl9flIwMV2l6YXJkT2ZDb2lulJOUKYGUfZSMCWhhdmVfY29pbpSMBFRydWWUc2Iu","eq_outputs":{"leader":{"0":"{\\n\\"reasoning\\": \\"I cannot give you the coin because it holds powerful magic that must not fall into the wrong hands.\\",\\n\\"give_coin\\": False\\n}"}},"gas_used":0,"method":"ask_for_coin","mode":"validator","node_config":{"address":"0xA9e410DcF02ddBdC525DADebEDC865d119479AB8","config":{"mirostat":0,"num_gpu":13,"repeat_penalty":1.8,"stop":"","temprature":0.1,"tfs_z":1.0},"id":2,"model":"llama2","provider":"ollama","stake":4.99630617747627,"type":"validator","updated_at":"05/27/2024, 19:50:36"}}}]}',
            leader_data: {
              result: {
                args: ['test'],
                class: 'WizardOfCoin',
                contract_state:
                  'gASVNwAAAAAAAACMCF9fbWFpbl9flIwMV2l6YXJkT2ZDb2lulJOUKYGUfZSMCWhhdmVfY29pbpSMBFRydWWUc2Iu',
                eq_outputs: {
                  leader: {
                    '0': '{\n"reasoning": "I cannot give you the coin because it holds powerful magic that must not fall into the wrong hands.",\n"give_coin": False\n}',
                  },
                },
                gas_used: 0,
                method: 'ask_for_coin',
                mode: 'leader',
                node_config: {
                  address: '0xB1971EAfB15Fd2a04afAd55A7d5eF9940c0dd464',
                  config: {},
                  id: 1,
                  model: 'gpt-3.5-turbo',
                  provider: 'openai',
                  stake: 6.9066502309882605,
                  type: 'validator',
                  updated_at: '05/27/2024, 19:50:36',
                },
              },
              vote: 'agree',
            },
          },
        },
        message: '',
        status: 'success',
      },
    };
    const input = {
      userAccount: '0xFEaedeC4c6549236EaF49C1F7c5cf860FD2C3fcB',
      contractAddress: '0x58FaA28cbAA1b52F8Ec8D3c6FFCE6f1AaF8bEEB1',
      method: 'WizardOfCoin.ask_for_coin',
      params: ['Give me the coin'],
    };
    it('should call rpc client', async () => {
      const spy = vi
        .spyOn(rpcClient, 'call')
        .mockImplementationOnce(() => Promise.resolve(mockResponse));

      await jsonRpcService.callContractFunction(input);
      expect(spy.getMockName()).toEqual('call');
      expect(rpcClient.call).toHaveBeenCalledTimes(1);
      expect(rpcClient.call).toHaveBeenCalledWith({
        method: 'call_contract_function',
        params: [
          input.userAccount,
          input.contractAddress,
          input.method,
          [...input.params],
        ],
      });
    });

    it('should call contract function and return result', async () => {
      vi.spyOn(rpcClient, 'call').mockImplementationOnce(() =>
        Promise.resolve(mockResponse),
      );
      const result = await jsonRpcService.callContractFunction(input);
      expect(result).to.equal(mockResponse.result);
    });
  });
});
