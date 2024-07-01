"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.areonNetwork = void 0;
const defineChain_js_1 = require("../../utils/chain/defineChain.js");
exports.areonNetwork = (0, defineChain_js_1.defineChain)({
    id: 463,
    name: 'Areon Network',
    nativeCurrency: { decimals: 18, name: 'AREA', symbol: 'AREA' },
    rpcUrls: {
        default: {
            http: ['https://mainnet-rpc.areon.network'],
            webSocket: ['wss://mainnet-ws.areon.network'],
        },
    },
    blockExplorers: {
        default: {
            name: 'Areonscan',
            url: 'https://areonscan.com',
        },
    },
    testnet: false,
});
//# sourceMappingURL=areonNetwork.js.map