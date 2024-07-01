import type { ErrorType } from '../errors/utils.js';
import type { GetSerializedTransactionType } from '../utils/transaction/getSerializedTransactionType.js';
import { type ParseTransactionErrorType as ParseTransactionErrorType_, type ParseTransactionReturnType as ParseTransactionReturnType_ } from '../utils/transaction/parseTransaction.js';
import type { OpStackTransactionSerialized, OpStackTransactionType, TransactionSerializableDeposit, TransactionSerializedDeposit } from './types/transaction.js';
export type ParseTransactionReturnType<TSerialized extends OpStackTransactionSerialized = OpStackTransactionSerialized, TType extends OpStackTransactionType = GetSerializedTransactionType<TSerialized>> = TSerialized extends TransactionSerializedDeposit ? TransactionSerializableDeposit : ParseTransactionReturnType_<TSerialized, TType>;
export type ParseTransactionErrorType = ParseTransactionErrorType_ | ErrorType;
export declare function parseTransaction<TSerialized extends OpStackTransactionSerialized>(serializedTransaction: TSerialized): ParseTransactionReturnType<TSerialized>;
//# sourceMappingURL=parsers.d.ts.map