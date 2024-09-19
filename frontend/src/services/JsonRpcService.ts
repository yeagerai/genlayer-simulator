import type { IRpcClient } from '@/clients/rpc';
import type { IJsonRpcService } from './IJsonRpcService';
import type {
  JsonRpcResult,
  JsonRPCRequest,
  JsonRPCResponse,
  GetContractStateRequest,
  GetContractStateResult,
  DeployContractRequest,
  GetContractSchemaRequest,
  GetDeployedContractSchemaRequest,
  CreateValidatorRequest,
  UpdateValidatorRequest,
  AddProviderRequest,
  UpdateProviderRequest,
  DeleteProviderRequest,
  TransactionItem,
  GetProvidersAndModelsData,
} from '@/types';

export class JsonRpcService implements IJsonRpcService {
  constructor(protected rpcClient: IRpcClient) {}
  /**
   * Retrieves the state of a contract at a specific address and method.
   *
   * @param {GetContractStateRequest} params - The parameters for the function.
   * @param {string} params.userAccount - The user account calling the function.
   * @param {string} params.contractAddress - The address of the contract.
   * @param {string} params.data - The encoded data including function name and arguments.
   * @return {Promise<JsonRpcResult<GetContractStateResult>>} A promise that resolves to the result of the contract state retrieval.
   */
  async getContractState({
    contractAddress,
    userAccount,
    data,
  }: GetContractStateRequest): Promise<JsonRpcResult<GetContractStateResult>> {
    const { result } = await this.rpcClient.call<GetContractStateResult>({
      method: 'call',
      params: [contractAddress, userAccount, data],
    });
    return result;
  }

  /**
   * Sends a signed transaction.
   *
   * @param {Object} signedTransaction - The signed transaction to be sent
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the result of the transaction being received and processed.
   */
  async sendTransaction(
    signedTransaction: string,
  ): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'send_raw_transaction',
      params: [signedTransaction],
    });
    return result;
  }

  /**
   * Deploys a new intelligent contract.
   *
   * @param {Object} params - The parameters for the function.
   * @param {string} params.userAccount - The user account calling the function.
   * @param {string} params.className - The name of the class for the contract.
   * @param {string} params.code - The code for the contract.
   * @param {string} params.constructorParams - The parameters for the contract constructor.
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the result of the contract deployment.
   */
  async deployContract({
    userAccount,
    className,
    code,
    constructorParams,
  }: DeployContractRequest): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'deploy_intelligent_contract',
      params: [userAccount, className, code, constructorParams],
    });
    return result;
  }

  /**
   * Retrieves the contract schema for the given code.
   *
   * @param {Object} params - The parameters for the function.
   * @param {string} params.code - The code for which the contract schema is retrieved.
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the contract schema.
   */
  async getContractSchema({
    code,
  }: GetContractSchemaRequest): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'get_contract_schema_for_code',
      params: [code],
    });
    return result;
  }
  /**
   * Retrieves the deployed contract schema for the given address.
   *
   * @param {Object} params - The parameters for the function.
   * @param {string} params.address - The address of the deployed contract.
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the deployed contract schema.
   */
  async getDeployedContractSchema({
    address,
  }: GetDeployedContractSchemaRequest): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'get_contract_schema',
      params: [address],
    });
    return result;
  }
  /**
   * Retrieves a list of validators from the JSON-RPC server.
   *
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the list of validators.
   */
  async getValidators(): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'get_all_validators',
      params: [],
    });
    return result;
  }

  /**
   * Retrieves a list of providers and models from the JSON-RPC server.
   *
   * @return {Promise<JsonRpcResult<GetProvidersAndModelsData>>} A promise that resolves to the list of providers and models.
   */
  async getProvidersAndModels(): Promise<
    JsonRpcResult<GetProvidersAndModelsData>
  > {
    const { result } = await this.rpcClient.call<GetProvidersAndModelsData>({
      method: 'get_providers_and_models',
      params: [],
    });
    return result;
  }

  /**
   * Adds a new provider on the JSON-RPC server.
   *
   * @param {Object} params - The parameters for adding the provider.
   * @param {string} params.provider - The name of the provider.
   * @param {string} params.model - The model name for the provider.
   * @param {Object} params.config - The configuration for the provider.
   * @param {string} params.plugin - The plugin name for the provider.
   * @param {Object} params.plugin_config - The plugin configuration for the provider.
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the result of adding the provider.
   */
  async addProvider({
    provider,
    model,
    config,
    plugin,
    plugin_config,
  }: AddProviderRequest): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'add_provider',
      params: [{ provider, model, config, plugin, plugin_config }],
    });
    return result;
  }

  /**
   * Updates an existing provider on the JSON-RPC server.
   *
   * @param {number} id - The ID of the provider to update.
   * @param {Object} params - The parameters for updating the provider.
   * @param {string} params.provider - The updated name of the provider.
   * @param {string} params.model - The updated model name for the provider.
   * @param {Object} params.config - The updated configuration for the provider.
   * @param {string} params.plugin - The updated plugin name for the provider.
   * @param {Object} params.plugin_config - The updated plugin configuration for the provider.
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the result of updating the provider.
   */
  async updateProvider({
    id,
    provider,
    model,
    config,
    plugin,
    plugin_config,
  }: UpdateProviderRequest): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'update_provider',
      params: [id, { provider, model, config, plugin, plugin_config }],
    });
    return result;
  }

  /**
   * Deletes a provider from the JSON-RPC server.
   *
   * @param {number} id - The ID of the provider to delete.
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the result of deleting the provider.
   */
  async deleteProvider({
    id,
  }: DeleteProviderRequest): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'delete_provider',
      params: [id],
    });
    return result;
  }

  /**
   * Creates a validator on the JSON-RPC server.
   *
   * @param {Object} params - The parameters for creating the validator.
   * @param {number} params.stake - The stake amount for the validator.
   * @param {string} params.provider - The provider for the validator.
   * @param {string} params.model - The model for the validator.
   * @param {any} params.config - The configuration for the validator.
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the result of the validator creation.
   */
  async createValidator({
    stake,
    provider,
    model,
    config,
  }: CreateValidatorRequest): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'create_validator',
      params: [stake, provider, model, config],
    });
    return result;
  }

  /**
   * Updates a validator on the JSON-RPC server.
   *
   * @param {Object} params - The parameters for updating the validator.
   * @param {string} params.address - The address of the validator.
   * @param {number} params.stake - The updated stake amount for the validator.
   * @param {string} params.provider - The updated provider for the validator.
   * @param {string} params.model - The updated model for the validator.
   * @param {any} params.config - The updated configuration for the validator.
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the result of the validator update.
   */
  async updateValidator({
    address,
    stake,
    provider,
    model,
    config,
  }: UpdateValidatorRequest): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'update_validator',
      params: [address, stake, provider, model, config],
    });
    return result;
  }
  /**
   * Deletes a validator on the JSON-RPC server.
   *
   * @param {Object} params - The parameters for deleting the validator.
   * @param {string} params.address - The address of the validator to delete.
   * @return {Promise<JsonRpcResult<any>>} A promise that resolves to the result of the validator deletion.
   */
  async deleteValidator({
    address,
  }: {
    address: string;
  }): Promise<JsonRpcResult<any>> {
    const { result } = await this.rpcClient.call({
      method: 'delete_validator',
      params: [address],
    });
    return result;
  }

  async getTransactionByHash(
    hash: string,
  ): Promise<JsonRpcResult<TransactionItem>> {
    const { result } = await this.rpcClient.call<TransactionItem>({
      method: 'get_transaction_by_hash',
      params: [`${hash}`],
    });
    return result;
  }

  /**
   * Calls a JSON-RPC method with the specified parameters and returns a promise that resolves to the JSON-RPC response.
   *
   * @param {JsonRPCRequest} request - The JSON-RPC request object containing the method and parameters.
   * @param {string} request.method - The name of the JSON-RPC method to call.
   * @param {any[]} request.params - The parameters to pass to the JSON-RPC method.
   * @return {Promise<JsonRPCResponse<any>>} A promise that resolves to the JSON-RPC response.
   */
  call({ method, params }: JsonRPCRequest): Promise<JsonRPCResponse<any>> {
    return this.rpcClient.call({ method, params });
  }
}
