import type { Address } from 'abitype';
import { type InvalidAddressErrorType } from '../errors/address.js';
import { type IsAddressErrorType } from '../utils/address/isAddress.js';
import type { ErrorType } from '../errors/utils.js';
import type { AccountSource, CustomSource, JsonRpcAccount, LocalAccount } from './types.js';
type GetAccountReturnType<TAccountSource extends AccountSource> = (TAccountSource extends Address ? JsonRpcAccount : never) | (TAccountSource extends CustomSource ? LocalAccount : never);
export type ToAccountErrorType = InvalidAddressErrorType | IsAddressErrorType | ErrorType;
/**
 * @description Creates an Account from a custom signing implementation.
 *
 * @returns A Local Account.
 */
export declare function toAccount<TAccountSource extends AccountSource>(source: TAccountSource): GetAccountReturnType<TAccountSource>;
export {};
//# sourceMappingURL=toAccount.d.ts.map