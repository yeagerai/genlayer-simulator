import { BaseError } from '../../errors/base.js';
export class TokenIsEthError extends BaseError {
    constructor() {
        super(['Token is an ETH token.', '', 'ETH token cannot be retrieved.'].join('\n'));
        Object.defineProperty(this, "name", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: 'TokenIsEthError'
        });
    }
}
//# sourceMappingURL=token-is-eth.js.map