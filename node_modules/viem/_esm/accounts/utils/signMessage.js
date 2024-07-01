import { hashMessage, } from '../../utils/signature/hashMessage.js';
import { serializeSignature, } from '../../utils/signature/serializeSignature.js';
import { sign } from './sign.js';
/**
 * @description Calculates an Ethereum-specific signature in [EIP-191 format](https://eips.ethereum.org/EIPS/eip-191):
 * `keccak256("\x19Ethereum Signed Message:\n" + len(message) + message))`.
 *
 * @returns The signature.
 */
export async function signMessage({ message, privateKey, }) {
    const signature = await sign({ hash: hashMessage(message), privateKey });
    return serializeSignature(signature);
}
//# sourceMappingURL=signMessage.js.map