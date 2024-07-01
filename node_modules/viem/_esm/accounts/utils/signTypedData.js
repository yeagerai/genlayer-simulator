import { hashTypedData, } from '../../utils/signature/hashTypedData.js';
import { serializeSignature, } from '../../utils/signature/serializeSignature.js';
import { sign } from './sign.js';
/**
 * @description Signs typed data and calculates an Ethereum-specific signature in [EIP-191 format](https://eips.ethereum.org/EIPS/eip-191):
 * `keccak256("\x19Ethereum Signed Message:\n" + len(message) + message))`.
 *
 * @returns The signature.
 */
export async function signTypedData(parameters) {
    const { privateKey, ...typedData } = parameters;
    const signature = await sign({
        hash: hashTypedData(typedData),
        privateKey,
    });
    return serializeSignature(signature);
}
//# sourceMappingURL=signTypedData.js.map