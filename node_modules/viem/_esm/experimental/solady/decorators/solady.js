import { signMessage, } from '../actions/signMessage.js';
import { signTypedData, } from '../actions/signTypedData.js';
/**
 * A suite of Actions based on [Solady contracts](https://github.com/Vectorized/solady).
 *
 * @example
 * import { createPublicClient, createWalletClient, http } from 'viem'
 * import { mainnet } from 'viem/chains'
 * import { soladyActions } from 'viem/experimental'
 *
 * const walletClient = createWalletClient({
 *   chain: mainnet,
 *   transport: http(),
 * }).extend(soladyActions())
 *
 * const result = await walletClient.signMessage({...})
 */
export function soladyActions(parameters = {}) {
    const { verifier } = parameters;
    return (client) => {
        return {
            signMessage: (parameters) => signMessage(client, { verifier, ...parameters }),
            signTypedData: (parameters) => signTypedData(client, { verifier, ...parameters }),
        };
    };
}
//# sourceMappingURL=solady.js.map