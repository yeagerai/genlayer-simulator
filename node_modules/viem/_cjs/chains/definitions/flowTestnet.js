"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.flowTestnet = void 0;
const defineChain_js_1 = require("../../utils/chain/defineChain.js");
exports.flowTestnet = (0, defineChain_js_1.defineChain)({
    id: 545,
    name: 'FlowEVM Testnet',
    nativeCurrency: {
        decimals: 18,
        name: 'Flow',
        symbol: 'FLOW',
    },
    rpcUrls: {
        default: {
            http: ['https://testnet.evm.nodes.onflow.org'],
        },
    },
    blockExplorers: {
        default: {
            name: 'Flow Diver',
            url: 'https://testnet.flowdiver.io',
        },
    },
});
//# sourceMappingURL=flowTestnet.js.map