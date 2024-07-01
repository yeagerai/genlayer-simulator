import { parseAccount } from '../../../accounts/utils/parseAccount.js';
import { AccountNotFoundError } from '../../../errors/account.js';
import { ChainNotFoundError } from '../../../errors/chain.js';
import { numberToHex } from '../../../utils/encoding/toHex.js';
import { getTransactionError } from '../../../utils/errors/getTransactionError.js';
/**
 * Requests the connected wallet to send a batch of calls.
 *
 * - Docs: https://viem.sh/experimental/eip5792/sendCalls
 * - JSON-RPC Methods: [`wallet_sendCalls`](https://eips.ethereum.org/EIPS/eip-5792)
 *
 * @param client - Client to use
 * @returns Transaction identifier. {@link SendCallsReturnType}
 *
 * @example
 * import { createWalletClient, custom } from 'viem'
 * import { mainnet } from 'viem/chains'
 * import { sendCalls } from 'viem/wallet'
 *
 * const client = createWalletClient({
 *   chain: mainnet,
 *   transport: custom(window.ethereum),
 * })
 * const id = await sendCalls(client, {
 *   account: '0xA0Cf798816D4b9b9866b5330EEa46a18382f251e',
 *   calls: [
 *     {
 *       data: '0xdeadbeef',
 *       to: '0x70997970c51812dc3a010c7d01b50e0d17dc79c8',
 *     },
 *     {
 *       to: '0x70997970c51812dc3a010c7d01b50e0d17dc79c8',
 *       value: 69420n,
 *     },
 *   ],
 * })
 */
export async function sendCalls(client, parameters) {
    const { account: account_ = client.account, calls, capabilities, chain = client.chain, version = '1.0', } = parameters;
    if (!account_)
        throw new AccountNotFoundError({
            docsPath: '/experimental/eip5792/sendCalls',
        });
    const account = parseAccount(account_);
    if (!chain)
        throw new ChainNotFoundError();
    try {
        return await client.request({
            method: 'wallet_sendCalls',
            params: [
                {
                    calls: calls.map((call) => ({
                        ...call,
                        value: call.value ? numberToHex(call.value) : undefined,
                    })),
                    capabilities,
                    chainId: numberToHex(chain.id),
                    from: account.address,
                    version,
                },
            ],
        }, { retryCount: 0 });
    }
    catch (err) {
        throw getTransactionError(err, {
            ...parameters,
            account,
            chain: parameters.chain,
        });
    }
}
//# sourceMappingURL=sendCalls.js.map