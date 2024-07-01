"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.modeTestnet = void 0;
const defineChain_js_1 = require("../../utils/chain/defineChain.js");
const sourceId = 11_155_111;
exports.modeTestnet = (0, defineChain_js_1.defineChain)({
    id: 919,
    name: 'Mode Testnet',
    nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
    rpcUrls: {
        default: {
            http: ['https://sepolia.mode.network'],
        },
    },
    blockExplorers: {
        default: {
            name: 'Blockscout',
            url: 'https://sepolia.explorer.mode.network',
            apiUrl: 'https://sepolia.explorer.mode.network/api',
        },
    },
    contracts: {
        multicall3: {
            address: '0xBAba8373113Fb7a68f195deF18732e01aF8eDfCF',
            blockCreated: 3019007,
        },
    },
    testnet: true,
    sourceId,
});
//# sourceMappingURL=modeTestnet.js.map