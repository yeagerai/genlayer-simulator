import type { ErrorType } from '../../errors/utils.js';
import type { Chain, ExtractChainFormatterReturnType } from '../../types/chain.js';
import type { RpcTransactionReceipt } from '../../types/rpc.js';
import type { TransactionReceipt } from '../../types/transaction.js';
import type { ExactPartial } from '../../types/utils.js';
import { type DefineFormatterErrorType } from './formatter.js';
export type FormattedTransactionReceipt<TChain extends Chain | undefined = undefined> = ExtractChainFormatterReturnType<TChain, 'transactionReceipt', TransactionReceipt>;
export declare const receiptStatuses: {
    readonly '0x0': "reverted";
    readonly '0x1': "success";
};
export type FormatTransactionReceiptErrorType = ErrorType;
export declare function formatTransactionReceipt(transactionReceipt: ExactPartial<RpcTransactionReceipt>): TransactionReceipt;
export type DefineTransactionReceiptErrorType = DefineFormatterErrorType | ErrorType;
export declare const defineTransactionReceipt: <TOverrideParameters, TOverrideReturnType, TExclude extends (keyof RpcTransactionReceipt | keyof TOverrideParameters)[] = []>({ exclude, format: overrides, }: {
    exclude?: TExclude | undefined;
    format: (_: TOverrideParameters) => TOverrideReturnType;
}) => {
    exclude: TExclude | undefined;
    format: (args: import("../../types/utils.js").Assign<ExactPartial<RpcTransactionReceipt>, TOverrideParameters>) => (import("../../types/utils.js").Assign<TransactionReceipt, TOverrideReturnType> extends infer T ? { [K in keyof T]: import("../../types/utils.js").Assign<TransactionReceipt, TOverrideReturnType>[K]; } : never) & { [_key in TExclude[number]]: never; };
    type: "transactionReceipt";
};
//# sourceMappingURL=transactionReceipt.d.ts.map