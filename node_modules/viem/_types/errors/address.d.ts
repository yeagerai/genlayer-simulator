import { BaseError } from './base.js';
export type InvalidAddressErrorType = InvalidAddressError & {
    name: 'InvalidAddressError';
};
export declare class InvalidAddressError extends BaseError {
    name: string;
    constructor({ address }: {
        address: string;
    });
}
//# sourceMappingURL=address.d.ts.map