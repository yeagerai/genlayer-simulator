// TODO(v3): checksum address.
import { AbiEventSignatureNotFoundError, DecodeLogDataMismatch, DecodeLogTopicsMismatch, } from '../../errors/abi.js';
import { decodeEventLog, } from './decodeEventLog.js';
/**
 * Extracts & decodes logs matching the provided signature(s) (`abi` + optional `eventName`)
 * from a set of opaque logs.
 *
 * @param parameters - {@link ParseEventLogsParameters}
 * @returns The logs. {@link ParseEventLogsReturnType}
 *
 * @example
 * import { createClient, http } from 'viem'
 * import { mainnet } from 'viem/chains'
 * import { parseEventLogs } from 'viem/op-stack'
 *
 * const client = createClient({
 *   chain: mainnet,
 *   transport: http(),
 * })
 *
 * const receipt = await getTransactionReceipt(client, {
 *   hash: '0xec23b2ba4bc59ba61554507c1b1bc91649e6586eb2dd00c728e8ed0db8bb37ea',
 * })
 *
 * const logs = parseEventLogs({ logs: receipt.logs })
 * // [{ args: { ... }, eventName: 'TransactionDeposited', ... }, ...]
 */
export function parseEventLogs({ abi, eventName, logs, strict = true, }) {
    return logs
        .map((log) => {
        try {
            const event = decodeEventLog({
                ...log,
                abi,
                strict,
            });
            if (eventName && !eventName.includes(event.eventName))
                return null;
            return { ...event, ...log };
        }
        catch (err) {
            let eventName;
            let isUnnamed;
            if (err instanceof AbiEventSignatureNotFoundError)
                return null;
            if (err instanceof DecodeLogDataMismatch ||
                err instanceof DecodeLogTopicsMismatch) {
                // If strict mode is on, and log data/topics do not match event definition, skip.
                if (strict)
                    return null;
                eventName = err.abiItem.name;
                isUnnamed = err.abiItem.inputs?.some((x) => !('name' in x && x.name));
            }
            // Set args to empty if there is an error decoding (e.g. indexed/non-indexed params mismatch).
            return { ...log, args: isUnnamed ? [] : {}, eventName };
        }
    })
        .filter(Boolean);
}
//# sourceMappingURL=parseEventLogs.js.map