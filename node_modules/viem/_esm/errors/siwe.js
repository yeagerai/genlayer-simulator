import { BaseError } from './base.js';
export class SiweInvalidMessageFieldError extends BaseError {
    constructor(parameters) {
        const { docsPath, field, metaMessages } = parameters;
        super(`Invalid Sign-In with Ethereum message field "${field}".`, {
            docsPath,
            docsSlug: 'TODO',
            metaMessages,
        });
        Object.defineProperty(this, "name", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: 'SiweInvalidMessageFieldError'
        });
    }
}
//# sourceMappingURL=siwe.js.map