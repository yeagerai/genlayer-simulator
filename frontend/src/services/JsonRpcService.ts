import type { IRpcClient } from '@/clients/rpc';
import type { IJsonRpcService } from './IJsonRpcService';
import type {
  GetContractStateRequest,
  GetContractStateResult,
  GetContractSchemaRequest,
  GetDeployedContractSchemaRequest,
  CreateValidatorRequest,
  UpdateValidatorRequest,
  TransactionItem,
} from '@/types';

export class JsonRpcService implements IJsonRpcService {
  constructor(protected rpcClient: IRpcClient) {}

  private async callRpcMethod<T>(
    method: string,
    params: any[],
    errorMessage: string,
  ): Promise<T | T[]> {
    const { result, error } = await this.rpcClient.call<T>({
      method,
      params,
    });
    if (error) {
      console.error(error.message, error.code);
      throw new Error(errorMessage);
    }
    return result;
  }

  async getContractState({
    contractAddress,
    userAccount,
    data,
  }: GetContractStateRequest): Promise<GetContractStateResult> {
    return this.callRpcMethod<GetContractStateResult>(
      'eth_call',
      [contractAddress, userAccount, data],
      'Error getting contract state',
    );
  }

  async sendTransaction(signedTransaction: string): Promise<any> {
    return this.callRpcMethod<any>(
      'eth_sendRawTransaction',
      [signedTransaction],
      'Error sending transaction',
    );
  }

  async getContractSchema({ code }: GetContractSchemaRequest): Promise<any> {
    return this.callRpcMethod<any>(
      'gen_getContractSchemaForCode',
      [code],
      'Error getting contract schema',
    );
  }

  async getDeployedContractSchema({
    address,
  }: GetDeployedContractSchemaRequest): Promise<any> {
    return this.callRpcMethod<any>(
      'gen_getContractSchema',
      [address],
      'Error getting deployed contract schema',
    );
  }

  async getValidators(): Promise<any> {
    return this.callRpcMethod<any>(
      'sim_getAllValidators',
      [],
      'Error getting validators',
    );
  }

  async getProvidersAndModels(): Promise<any> {
    return this.callRpcMethod<any>(
      'sim_getProvidersAndModels',
      [],
      'Error getting providers and models',
    );
  }

  async createValidator({
    stake,
    provider,
    model,
    config,
  }: CreateValidatorRequest): Promise<any> {
    return this.callRpcMethod<any>(
      'sim_createValidator',
      [stake, provider, model, config],
      'Error creating validator',
    );
  }

  async updateValidator({
    address,
    stake,
    provider,
    model,
    config,
  }: UpdateValidatorRequest): Promise<any> {
    return this.callRpcMethod<any>(
      'sim_updateValidator',
      [address, stake, provider, model, config],
      'Error updating validator',
    );
  }

  async deleteValidator({ address }: { address: string }): Promise<any> {
    return this.callRpcMethod<any>(
      'sim_deleteValidator',
      [address],
      'Error deleting validator',
    );
  }

  async getTransactionByHash(txId: string): Promise<TransactionItem> {
    return this.callRpcMethod<TransactionItem>(
      'eth_getTransactionByHash',
      [String(txId)],
      'Error getting transaction by ID',
    ) as Promise<TransactionItem>;
  }
}
