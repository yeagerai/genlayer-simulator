import type { ErrorType } from '../../errors/utils.js';
import type { ByteArray, Hex } from '../../types/misc.js';
export type ConcatReturnType<TValue extends Hex | ByteArray> = TValue extends Hex ? Hex : ByteArray;
export type ConcatErrorType = ConcatBytesErrorType | ConcatHexErrorType | ErrorType;
export declare function concat<TValue extends Hex | ByteArray>(values: readonly TValue[]): ConcatReturnType<TValue>;
export type ConcatBytesErrorType = ErrorType;
export declare function concatBytes(values: readonly ByteArray[]): ByteArray;
export type ConcatHexErrorType = ErrorType;
export declare function concatHex(values: readonly Hex[]): Hex;
//# sourceMappingURL=concat.d.ts.map