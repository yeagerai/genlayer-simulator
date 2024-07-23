export interface JsonRpcResult<T> {
  data: T
  message: string
  status: string
}

export interface GetContractStateResult extends Record<string, any> {}

export interface CallContractFunctionResult {
  execution_output: {
    consensus_data: string
    leader_data: {
      result: {
        args: any[]
        class: string
        contract_state: string
        eq_outputs: {
          leader: Record<number, string>
        }
        gas_used: number
        method: string
        mode: string
        node_config: {
          address: string
          config: any
          id: number
          model: string
          provider: string
          stake: number
          type: string
          updated_at: string
        }
      }

      vote: string
    }
  }
}
