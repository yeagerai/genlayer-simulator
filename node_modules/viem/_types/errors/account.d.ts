import { BaseError } from './base.js';
export type AccountNotFoundErrorType = AccountNotFoundError & {
    name: 'AccountNotFoundError';
};
export declare class AccountNotFoundError extends BaseError {
    name: string;
    constructor({ docsPath }?: {
        docsPath?: string | undefined;
    });
}
//# sourceMappingURL=account.d.ts.map