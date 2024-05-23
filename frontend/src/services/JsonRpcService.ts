import { rpcClient } from '@/utils'
import type { IJsonRPCService } from './IJsonRpcService'
import type { JsonRPCRequest, JsonRPCResponse, JsonRPCResult } from '@/types'

export class JsonRprService implements IJsonRPCService {
  /**
   * Retrieves the state of a contract at a specific address and method.
   *
   * @param {Object} params - The parameters for the function.
   * @param {string} params.contractAddress - The address of the contract.
   * @param {string} params.method - The method of the contract.
   * @param {any[]} params.methodArguments - The arguments for the method.
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the result of the contract state retrieval.
   */
  async getContractState({
    contractAddress,
    method,
    methodArguments
  }: {
    contractAddress: string
    method: string
    methodArguments: any[]
  }): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'get_contract_state',
      params: [contractAddress, method, methodArguments]
    })
    return result
  }
  /**
   * Calls a contract function and returns the result.
   *
   * @param {Object} params - The parameters for the function.
   * @param {string} params.userAccount - The user account calling the function.
   * @param {string} params.contractAddress - The address of the contract.
   * @param {string} params.method - The method of the contract.
   * @param {any[]} params.params - The parameters for the method.
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the result of the contract function call.
   */
  async callContractFunction({
    userAccount,
    contractAddress,
    method,
    params
  }: {
    userAccount: string
    contractAddress: string
    method: string
    params: any[]
  }): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'call_contract_function',
      params: [userAccount, contractAddress, method, params]
    })
    return result
  }
  
  /**
   * Deploys a new intelligent contract.
   *
   * @param {Object} params - The parameters for the function.
   * @param {string} params.userAccount - The user account calling the function.
   * @param {string} params.className - The name of the class for the contract.
   * @param {string} params.code - The code for the contract.
   * @param {string} params.constructorParams - The parameters for the contract constructor.
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the result of the contract deployment.
   */
  async deployContract({
    userAccount,
    className,
    code,
    constructorParams
  }: {
    userAccount: string
    className: string
    code: string
    constructorParams: string
  }): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'deploy_intelligent_contract',
      params: [userAccount, className, code, constructorParams]
    })
    return result
  }
  
  /**
   * Retrieves the contract schema for the given code.
   *
   * @param {Object} params - The parameters for the function.
   * @param {string} params.code - The code for which the contract schema is retrieved.
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the contract schema.
   */
  async getContractSchema({ code }: { code: string }): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'get_icontract_schema_for_code',
      params: [code]
    })
    return result
  }
  /**
   * Retrieves the deployed contract schema for the given address.
   *
   * @param {Object} params - The parameters for the function.
   * @param {string} params.address - The address of the deployed contract.
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the deployed contract schema.
   */
  async  getDeployedContractSchema({ address }: { address: string }): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'get_icontract_schema',
      params: [address]
    })
    return result
  }
  /**
   * Retrieves a list of validators from the JSON-RPC server.
   *
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the list of validators.
   */
  async  getValidators(): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'get_all_validators',
      params: []
    })
    return result
  }
  
  /**
   * Retrieves a list of providers and models from the JSON-RPC server.
   *
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the list of providers and models.
   */
  async  getProvidersAndModels(): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'get_providers_and_models',
      params: []
    })
    return result
  }
  /**
   * Creates a validator on the JSON-RPC server.
   *
   * @param {Object} params - The parameters for creating the validator.
   * @param {number} params.stake - The stake amount for the validator.
   * @param {string} params.provider - The provider for the validator.
   * @param {string} params.model - The model for the validator.
   * @param {any} params.config - The configuration for the validator.
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the result of the validator creation.
   */
  async createValidator({
    stake,
    provider,
    model,
    config
  }: {
    stake: number
    provider: string
    model: string
    config: any
  }): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'create_validator',
      params: [stake, provider, model, config]
    })
    return result
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
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the result of the validator update.
   */
  async updateValidator({
    address,
    stake,
    provider,
    model,
    config
  }: {
    address: string
    stake: number
    provider: string
    model: string
    config: any
  }): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'update_validator',
      params: [address, stake, provider, model, config]
    })
    return result
  }
  /**
   * Deletes a validator on the JSON-RPC server.
   *
   * @param {Object} params - The parameters for deleting the validator.
   * @param {string} params.address - The address of the validator to delete.
   * @return {Promise<JsonRPCResult<any>>} A promise that resolves to the result of the validator deletion.
   */
  async deleteValidator({ address }: { address: string }): Promise<JsonRPCResult<any>> {
    const { result } = await rpcClient.call({
      method: 'delete_validator',
      params: [address]
    })
    return result
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
    return rpcClient.call({ method, params })
  }
}