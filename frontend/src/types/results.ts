export interface JsonRpcResult<T> {
  data: T;
  message: string;
  status: string;
}

export interface GetContractStateResult extends Record<string, any> {}
