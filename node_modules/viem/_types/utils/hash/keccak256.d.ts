import type { ErrorType } from '../../errors/utils.js';
import type { ByteArray, Hex } from '../../types/misc.js';
import { type IsHexErrorType } from '../data/isHex.js';
import { type ToBytesErrorType } from '../encoding/toBytes.js';
import { type ToHexErrorType } from '../encoding/toHex.js';
type To = 'hex' | 'bytes';
export type Keccak256Hash<TTo extends To> = (TTo extends 'bytes' ? ByteArray : never) | (TTo extends 'hex' ? Hex : never);
export type Keccak256ErrorType = IsHexErrorType | ToBytesErrorType | ToHexErrorType | ErrorType;
export declare function keccak256<TTo extends To = 'hex'>(value: Hex | ByteArray, to_?: TTo | undefined): Keccak256Hash<TTo>;
export {};
//# sourceMappingURL=keccak256.d.ts.map