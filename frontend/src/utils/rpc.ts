const JSON_RPC_SERVER_URL = import.meta.env.VITE_JSON_RPC_SERVER_URL
import { v4 as uuidv4 } from 'uuid'
export interface JsonRPCParams {
  method: string
  params: any[]
}

export const rpcClient = {
  call: async ({ method, params }: JsonRPCParams) => {
    const requestId = uuidv4()
    const data = {
      jsonrpc: '2.0',
      method,
      params,
      id: requestId
    }
    const response = await fetch(JSON_RPC_SERVER_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    return response.json()
  }
}
