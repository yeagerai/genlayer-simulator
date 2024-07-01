"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ReceiptContainsNoWithdrawalsError = exports.GameNotFoundError = void 0;
const base_js_1 = require("../../errors/base.js");
class GameNotFoundError extends base_js_1.BaseError {
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
exports.GameNotFoundError = GameNotFoundError;
class ReceiptContainsNoWithdrawalsError extends base_js_1.BaseError {
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
exports.ReceiptContainsNoWithdrawalsError = ReceiptContainsNoWithdrawalsError;
//# sourceMappingURL=withdrawal.js.map