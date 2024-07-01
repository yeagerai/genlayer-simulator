import type { GetSerializedTransactionType } from '../utils/transaction/getSerializedTransactionType.js';
import { type ParseTransactionReturnType as ParseTransactionReturnType_ } from '../utils/transaction/parseTransaction.js';
import type { CeloTransactionSerialized, CeloTransactionType, TransactionSerializableCIP42, TransactionSerializedCIP42 } from './types.js';
export type ParseTransactionReturnType<TSerialized extends CeloTransactionSerialized = CeloTransactionSerialized, TType extends CeloTransactionType = GetSerializedTransactionType<TSerialized>> = TSerialized extends TransactionSerializedCIP42 ? TransactionSerializableCIP42 : ParseTransactionReturnType_<TSerialized, TType>;
export declare function parseTransaction<TSerialized extends CeloTransactionSerialized>(serializedTransaction: TSerialized): ParseTransactionReturnType<TSerialized>;
//# sourceMappingURL=parsers.d.ts.map