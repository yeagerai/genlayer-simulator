import type { Chain } from '../types/chain.js';
import { BaseError } from './base.js';
export type ChainDoesNotSupportContractErrorType = ChainDoesNotSupportContract & {
    name: 'ChainDoesNotSupportContract';
};
export declare class ChainDoesNotSupportContract extends BaseError {
    name: string;
    constructor({ blockNumber, chain, contract, }: {
        blockNumber?: bigint | undefined;
        chain: Chain;
        contract: {
            name: string;
            blockCreated?: number | undefined;
        };
    });
}
export type ChainMismatchErrorType = ChainMismatchError & {
    name: 'ChainMismatchError';
};
export declare class ChainMismatchError extends BaseError {
    name: string;
    constructor({ chain, currentChainId, }: {
        chain: Chain;
        currentChainId: number;
    });
}
export type ChainNotFoundErrorType = ChainNotFoundError & {
    name: 'ChainNotFoundError';
};
export declare class ChainNotFoundError extends BaseError {
    name: string;
    constructor();
}
export type ClientChainNotConfiguredErrorType = ClientChainNotConfiguredError & {
    name: 'ClientChainNotConfiguredError';
};
export declare class ClientChainNotConfiguredError extends BaseError {
    name: string;
    constructor();
}
export type InvalidChainIdErrorType = InvalidChainIdError & {
    name: 'InvalidChainIdError';
};
export declare class InvalidChainIdError extends BaseError {
    name: string;
    constructor({ chainId }: {
        chainId?: number | undefined;
    });
}
//# sourceMappingURL=chain.d.ts.map