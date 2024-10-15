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
    abi: [
      {
        inputs: [
          {
            name: 'initial_storage',
            type: 'string',
          },
        ],
        type: 'constructor',
      },
      {
        inputs: [],
        name: 'get_storage',
        outputs: 'string',
        type: 'function',
      },
      {
        inputs: [
          {
            name: 'update',
            type: 'string',
          },
        ],
        name: 'new_storage',
        outputs: '',
        type: 'function',
      },
    ],
  };

  const mockDeploymentTx: TransactionItem = {
    contractAddress: mockContractAddress,
    localContractId: mockContractId,
    hash: '0x123',
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
