import type { ErrorType } from '../../errors/utils.js';
import type { ByteArray, Hex } from '../../types/misc.js';
import { type IsHexErrorType } from '../data/isHex.js';
import { type ToBytesErrorType } from '../encoding/toBytes.js';
import { type ToHexErrorType } from '../encoding/toHex.js';
type To = 'hex' | 'bytes';
export type Ripemd160Hash<TTo extends To> = (TTo extends 'bytes' ? ByteArray : never) | (TTo extends 'hex' ? Hex : never);
export type Ripemd160ErrorType = IsHexErrorType | ToBytesErrorType | ToHexErrorType | ErrorType;
export declare function ripemd160<TTo extends To = 'hex'>(value: Hex | ByteArray, to_?: TTo | undefined): Ripemd160Hash<TTo>;
export {};
//# sourceMappingURL=ripemd160.d.ts.map