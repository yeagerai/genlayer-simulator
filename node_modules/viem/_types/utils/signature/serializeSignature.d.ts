import type { ErrorType } from '../../errors/utils.js';
import type { Hex, Signature } from '../../types/misc.js';
import { type HexToBigIntErrorType } from '../encoding/fromHex.js';
import type { ToHexErrorType } from '../encoding/toHex.js';
export type SerializeSignatureErrorType = HexToBigIntErrorType | ToHexErrorType | ErrorType;
/**
 * @description Converts a signature into hex format.
 *
 * @param signature The signature to convert.
 * @returns The signature in hex format.
 *
 * @example
 * serializeSignature({
 *   r: '0x6e100a352ec6ad1b70802290e18aeed190704973570f3b8ed42cb9808e2ea6bf',
 *   s: '0x4a90a229a244495b41890987806fcbd2d5d23fc0dbe5f5256c2613c039d76db8',
 *   yParity: 1
 * })
 * // "0x6e100a352ec6ad1b70802290e18aeed190704973570f3b8ed42cb9808e2ea6bf4a90a229a244495b41890987806fcbd2d5d23fc0dbe5f5256c2613c039d76db81c"
 */
export declare function serializeSignature({ r, s, v, yParity }: Signature): Hex;
//# sourceMappingURL=serializeSignature.d.ts.map