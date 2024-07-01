import { BaseError } from '../../errors/base.js';
export class InvalidEip712TransactionError extends BaseError {
    constructor() {
        super([
            'Transaction is not an EIP712 transaction.',
            '',
            'Transaction must:',
            '  - include `type: "eip712"`',
            '  - include one of the following: `customSignature`, `paymaster`, `paymasterInput`, `gasPerPubdata`, `factoryDeps`',
        ].join('\n'));
        Object.defineProperty(this, "name", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: 'InvalidEip712TransactionError'
        });
    }
}
//# sourceMappingURL=transaction.js.map