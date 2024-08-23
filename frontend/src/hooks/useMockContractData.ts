import { type DeployedContract, type TransactionItem } from '@/types';

export function useMockContractData() {
  const mockContractId = '1a621cad-1cfd-4dbd-892a-f6bbde7a2fab';
  const mockContractAddress = '0x3F9Fb6C6aBaBD0Ae6cB27c513E7b0fE4C0B3E9C8';

  const mockDeployedContract: DeployedContract = {
    address: mockContractAddress,
    contractId: mockContractId,
    defaultState: '{}',
  };

  const mockContractSchema = {
    class: 'Storage',
    methods: {
      __init__: {
        inputs: {
          initial_storage: 'str',
        },
        output: 'None',
      },
      get_storage: {
        inputs: {},
        output: 'str',
      },
      update_storage: {
        inputs: {
          new_storage: 'str',
        },
        output: '',
      },
    },
  };

  const mockDeploymentTx: TransactionItem = {
    contractAddress: mockContractAddress,
    localContractId: mockContractId,
    txId: 1,
    type: 'deploy',
    status: 'FINALIZED',
    data: {},
  };

  return {
    mockContractId,
    mockDeployedContract,
    mockContractSchema,
    mockDeploymentTx,
  };
}
