import type { ErrorType } from '../../errors/utils.js';
import type { Hex, Signature } from '../../types/misc.js';
import { type ToHexErrorType } from '../../utils/encoding/toHex.js';
export type SignParameters = {
    hash: Hex;
    privateKey: Hex;
};
export type SignReturnType = Signature;
export type SignErrorType = ToHexErrorType | ErrorType;
/**
 * @description Signs a hash with a given private key.
 *
 * @param hash The hash to sign.
 * @param privateKey The private key to sign with.
 *
 * @returns The signature.
 */
export declare function sign({ hash, privateKey, }: SignParameters): Promise<SignReturnType>;
//# sourceMappingURL=sign.d.ts.map