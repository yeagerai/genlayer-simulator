"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.zkSyncTestnet = void 0;
const defineChain_js_1 = require("../../utils/chain/defineChain.js");
const chainConfig_js_1 = require("../../zksync/chainConfig.js");
exports.zkSyncTestnet = (0, defineChain_js_1.defineChain)({
    ...chainConfig_js_1.chainConfig,
    id: 280,
    name: 'zkSync Era Testnet',
    network: 'zksync-era-testnet',
    nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
    rpcUrls: {
        default: {
            http: ['https://testnet.era.zksync.dev'],
            webSocket: ['wss://testnet.era.zksync.dev/ws'],
        },
    },
    blockExplorers: {
        default: {
            name: 'zkExplorer',
            url: 'https://goerli.explorer.zksync.io',
        },
    },
    contracts: {
        multicall3: {
            address: '0xF9cda624FBC7e059355ce98a31693d299FACd963',
        },
    },
    testnet: true,
});
//# sourceMappingURL=zkSyncTestnet.js.map