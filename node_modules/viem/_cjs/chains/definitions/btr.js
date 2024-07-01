"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.btr = void 0;
const defineChain_js_1 = require("../../utils/chain/defineChain.js");
exports.btr = (0, defineChain_js_1.defineChain)({
    id: 200901,
    name: 'Bitlayer',
    nativeCurrency: {
        name: 'Ether',
        symbol: 'ETH',
        decimals: 18,
    },
    rpcUrls: {
        default: {
            http: [
                'https://rpc.bitlayer.org',
                'https://rpc.bitlayer-rpc.com',
                'https://rpc.ankr.com/bitlayer',
            ],
            webSocket: ['wss://ws.bitlayer.org', 'wss://ws.bitlayer-rpc.com'],
        },
    },
    blockExplorers: {
        default: {
            name: 'btrscan',
            url: 'https://www.btrscan.com',
            apiUrl: 'https://www.btrscan.com/apis',
        },
    },
});
//# sourceMappingURL=btr.js.map