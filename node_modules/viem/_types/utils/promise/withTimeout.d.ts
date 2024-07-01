import type { ErrorType } from '../../errors/utils.js';
export type WithTimeoutErrorType = ErrorType;
export declare function withTimeout<TData>(fn: ({ signal, }: {
    signal: AbortController['signal'] | null;
}) => Promise<TData>, { errorInstance, timeout, signal, }: {
    errorInstance?: Error | undefined;
    timeout: number;
    signal?: boolean | undefined;
}): Promise<TData>;
//# sourceMappingURL=withTimeout.d.ts.map