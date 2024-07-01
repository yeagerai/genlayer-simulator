import { type HttpRequestErrorType as HttpRequestErrorType_, type TimeoutErrorType } from '../../errors/request.js';
import type { ErrorType } from '../../errors/utils.js';
import type { RpcRequest, RpcResponse } from '../../types/rpc.js';
import { type WithTimeoutErrorType } from '../promise/withTimeout.js';
export type HttpRpcClientOptions = {
    /** Request configuration to pass to `fetch`. */
    fetchOptions?: Omit<RequestInit, 'body'> | undefined;
    /** A callback to handle the request. */
    onRequest?: ((request: Request) => Promise<void> | void) | undefined;
    /** A callback to handle the response. */
    onResponse?: ((response: Response) => Promise<void> | void) | undefined;
    /** The timeout (in ms) for the request. */
    timeout?: number | undefined;
};
export type HttpRequestParameters<TBody extends RpcRequest | RpcRequest[] = RpcRequest> = {
    /** The RPC request body. */
    body: TBody;
    /** Request configuration to pass to `fetch`. */
    fetchOptions?: HttpRpcClientOptions['fetchOptions'] | undefined;
    /** A callback to handle the response. */
    onRequest?: ((request: Request) => Promise<void> | void) | undefined;
    /** A callback to handle the response. */
    onResponse?: ((response: Response) => Promise<void> | void) | undefined;
    /** The timeout (in ms) for the request. */
    timeout?: HttpRpcClientOptions['timeout'] | undefined;
};
export type HttpRequestReturnType<TBody extends RpcRequest | RpcRequest[] = RpcRequest> = TBody extends RpcRequest[] ? RpcResponse[] : RpcResponse;
export type HttpRequestErrorType = HttpRequestErrorType_ | TimeoutErrorType | WithTimeoutErrorType | ErrorType;
export type HttpRpcClient = {
    request<TBody extends RpcRequest | RpcRequest[]>(params: HttpRequestParameters<TBody>): Promise<HttpRequestReturnType<TBody>>;
};
export declare function getHttpRpcClient(url: string, options?: HttpRpcClientOptions): HttpRpcClient;
//# sourceMappingURL=http.d.ts.map