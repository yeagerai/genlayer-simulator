import type { IRpcClient } from '@/clients/rpc';
import type { IJsonRpcService } from './IJsonRpcService';
import type {
  GetContractStateRequest,
  GetContractStateResult,
  DeployContractRequest,
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

  async deployContract({
    userAccount,
    className,
    code,
    constructorParams,
  }: DeployContractRequest): Promise<any> {
    return this.callRpcMethod<any>(
      'deploy_intelligent_contract',
      [userAccount, className, code, constructorParams],
      'Error deploying contract',
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
      'get_all_validators',
      [],
      'Error getting validators',
    );
  }

  async getProvidersAndModels(): Promise<any> {
    return this.callRpcMethod<any>(
      'get_providers_and_models',
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
      'create_validator',
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
      'update_validator',
      [address, stake, provider, model, config],
      'Error updating validator',
    );
  }

  async deleteValidator({ address }: { address: string }): Promise<any> {
    return this.callRpcMethod<any>(
      'delete_validator',
      [address],
      'Error deleting validator',
    );
  }

  async getTransactionById(txId: number): Promise<TransactionItem> {
    return this.callRpcMethod<TransactionItem>(
      'eth_getTransactionById',
      [txId],
      'Error getting transaction by ID',
    ) as Promise<TransactionItem>;
  }
}
