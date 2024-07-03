import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts'

export const getAccountFromPrivatekey = (privateKey: `0x${string}`) => {
    return privateKeyToAccount(privateKey)
}

export const getPrivateKey = () => {
    return generatePrivateKey()
}

