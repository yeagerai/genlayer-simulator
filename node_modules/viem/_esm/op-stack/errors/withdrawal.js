import { BaseError } from '../../errors/base.js';
export class GameNotFoundError extends BaseError {
    constructor() {
        super('Dispute game not found.');
        Object.defineProperty(this, "name", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: 'GameNotFoundError'
        });
    }
}
export class ReceiptContainsNoWithdrawalsError extends BaseError {
    constructor({ hash }) {
        super(`The provided transaction receipt with hash "${hash}" contains no withdrawals.`);
        Object.defineProperty(this, "name", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: 'ReceiptContainsNoWithdrawalsError'
        });
    }
}
//# sourceMappingURL=withdrawal.js.map