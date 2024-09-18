export interface JsonRpcResult<T> {
  data: T;
  message: string;
  status: string;
}

export interface GetContractStateResult extends Record<string, any> {}

export interface GetProvidersAndModelsData
  extends Array<{
    config: Record<string, any>;
    id: number;
    model: string;
    plugin: string;
    plugin_config: Record<string, any>;
    provider: string;
  }> {}
