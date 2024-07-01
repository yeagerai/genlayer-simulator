"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.opBNBTestnet = void 0;
const defineChain_js_1 = require("../../utils/chain/defineChain.js");
exports.opBNBTestnet = (0, defineChain_js_1.defineChain)({
    id: 5611,
    name: 'opBNB Testnet',
    nativeCurrency: {
        decimals: 18,
        name: 'tBNB',
        symbol: 'tBNB',
    },
    rpcUrls: {
        default: { http: ['https://opbnb-testnet-rpc.bnbchain.org'] },
    },
    blockExplorers: {
        default: {
            name: 'opbnbscan',
            url: 'https://testnet.opbnbscan.com',
        },
    },
    contracts: {
        multicall3: {
            address: '0xcA11bde05977b3631167028862bE2a173976CA11',
            blockCreated: 3705108,
        },
    },
    testnet: true,
});
//# sourceMappingURL=opBNBTestnet.js.map