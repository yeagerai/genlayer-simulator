import type { ErrorType } from '../errors/utils.js';
type PollOptions<TData> = {
    emitOnBegin?: boolean | undefined;
    initialWaitTime?: ((data: TData | void) => Promise<number>) | undefined;
    interval: number;
};
export type PollErrorType = ErrorType;
/**
 * @description Polls a function at a specified interval.
 */
export declare function poll<TData>(fn: ({ unpoll }: {
    unpoll: () => void;
}) => Promise<TData | void>, { emitOnBegin, initialWaitTime, interval }: PollOptions<TData>): () => boolean;
export {};
//# sourceMappingURL=poll.d.ts.map