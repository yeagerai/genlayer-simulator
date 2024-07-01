import type { ErrorType } from '../../errors/utils.js';
import type { ByteArray, Hex } from '../../types/misc.js';
type TrimOptions = {
    dir?: 'left' | 'right' | undefined;
};
export type TrimReturnType<TValue extends ByteArray | Hex> = TValue extends Hex ? Hex : ByteArray;
export type TrimErrorType = ErrorType;
export declare function trim<TValue extends ByteArray | Hex>(hexOrBytes: TValue, { dir }?: TrimOptions): TrimReturnType<TValue>;
export {};
//# sourceMappingURL=trim.d.ts.map