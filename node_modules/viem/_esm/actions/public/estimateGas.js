import { parseAccount, } from '../../accounts/utils/parseAccount.js';
import { numberToHex, } from '../../utils/encoding/toHex.js';
import { getEstimateGasError, } from '../../utils/errors/getEstimateGasError.js';
import { extract } from '../../utils/formatters/extract.js';
import { formatTransactionRequest, } from '../../utils/formatters/transactionRequest.js';
import { serializeStateOverride } from '../../utils/stateOverride.js';
import { assertRequest, } from '../../utils/transaction/assertRequest.js';
import { prepareTransactionRequest, } from '../wallet/prepareTransactionRequest.js';
/**
 * Estimates the gas necessary to complete a transaction without submitting it to the network.
 *
 * - Docs: https://viem.sh/docs/actions/public/estimateGas
 * - JSON-RPC Methods: [`eth_estimateGas`](https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_estimategas)
 *
 * @param client - Client to use
 * @param parameters - {@link EstimateGasParameters}
 * @returns The gas estimate (in wei). {@link EstimateGasReturnType}
 *
 * @example
 * import { createPublicClient, http, parseEther } from 'viem'
 * import { mainnet } from 'viem/chains'
 * import { estimateGas } from 'viem/public'
 *
 * const client = createPublicClient({
 *   chain: mainnet,
 *   transport: http(),
 * })
 * const gasEstimate = await estimateGas(client, {
 *   account: '0xA0Cf798816D4b9b9866b5330EEa46a18382f251e',
 *   to: '0x70997970c51812dc3a010c7d01b50e0d17dc79c8',
 *   value: parseEther('1'),
 * })
 */
export async function estimateGas(client, args) {
    const account_ = args.account ?? client.account;
    const account = account_ ? parseAccount(account_) : undefined;
    try {
        const { accessList, blobs, blobVersionedHashes, blockNumber, blockTag, data, gas, gasPrice, maxFeePerBlobGas, maxFeePerGas, maxPriorityFeePerGas, nonce, to, value, stateOverride, ...rest } = (await prepareTransactionRequest(client, {
            ...args,
            parameters: 
            // Some RPC Providers do not compute versioned hashes from blobs. We will need
            // to compute them.
            account?.type === 'local' ? undefined : ['blobVersionedHashes'],
        }));
        const blockNumberHex = blockNumber ? numberToHex(blockNumber) : undefined;
        const block = blockNumberHex || blockTag;
        const rpcStateOverride = serializeStateOverride(stateOverride);
        assertRequest(args);
        const chainFormat = client.chain?.formatters?.transactionRequest?.format;
        const format = chainFormat || formatTransactionRequest;
        const request = format({
            // Pick out extra data that might exist on the chain's transaction request type.
            ...extract(rest, { format: chainFormat }),
            from: account?.address,
            accessList,
            blobs,
            blobVersionedHashes,
            data,
            gas,
            gasPrice,
            maxFeePerBlobGas,
            maxFeePerGas,
            maxPriorityFeePerGas,
            nonce,
            to,
            value,
        });
        const balance = await client.request({
            method: 'eth_estimateGas',
            params: rpcStateOverride
                ? [request, block ?? 'latest', rpcStateOverride]
                : block
                    ? [request, block]
                    : [request],
        });
        return BigInt(balance);
    }
    catch (err) {
        throw getEstimateGasError(err, {
            ...args,
            account,
            chain: client.chain,
        });
    }
}
//# sourceMappingURL=estimateGas.js.map