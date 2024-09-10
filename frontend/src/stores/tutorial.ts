import { defineStore } from 'pinia';
import { useContractsStore } from './contracts';
import { useNodeStore } from './node';
import { useTransactionsStore } from './transactions';
import { useMockContractData } from '@/hooks/useMockContractData';
import contractBlob from '@/assets/examples/contracts/storage.py?raw';

const { mockContractId, mockDeployedContract, mockDeploymentTx } =
  useMockContractData();

const contractFunctionLogs = [
  {
    function: 'call_contract_function',
    trace_id: 'ljpjjd852',
    response: {
      status: 'info',
      message: 'Starting...',
      data: {},
    },
  },
  {
    function: 'call_contract_function',
    trace_id: 'ljpjjd852',
    response: {
      status: 'info',
      message: 'db connection created',
      data: {},
    },
  },
  {
    function: 'call_contract_function',
    trace_id: 'ljpjjd852',
    response: {
      status: 'info',
      message: 'Data formatted',
      data: {},
    },
  },
  {
    function: 'call_contract_function',
    trace_id: 'ljpjjd852',
    response: {
      status: 'info',
      message:
        'Transaction sent from 0xCcD1af1388b74Bb9DFc232292eD1bfc6d21BD3FC to 0x4Fb3673Ab7274ebBA6ff38EDB1ca5Bd0cd06C0FD...',
      data: {},
    },
  },
  "Selected Leader: {'id': 2, 'address': '0xBfE0B24B9C86D54384BAdC0426C7A7BDe7f71DFA', 'stake': 1.6300447758707397, 'provider': 'openai', 'model': 'gpt-4o-mini', 'config': {}, 'updated_at': '06/17/2024, 21:47:04'}...",
  "Selected Validators: [{'id': 10, 'address': '0x1Da8FEfaD3d6A90F1BD49d03eCbb2E50aEB6C67A', 'stake': 3.0603317919753037, 'provider': 'openai', 'model': 'gpt-4o-mini', 'config': {}, 'updated_at': '06/17/2024, 21:47:05'}, {'id': 6, 'address': '0xbe109fB11baCa678DFCc3623296CAaf3a3E4cd6f', 'stake': 1.3238056014305584, 'provider': 'ollama', 'model': 'llama2', 'config': {'seed': 961179, 'stop': '', 'tfs_z': 1.9, 'top_k': 59, 'num_gpu': 1, 'num_gqa': 10, 'mirostat': 1, 'num_thread': 1, 'temprature': 0.0, 'mirostat_tau': 2.3, 'repeat_penalty': 1.5}, 'updated_at': '06/17/2024, 21:47:04'}, {'id': 7, 'address': '0xeD6EF403EC83b8Dd8feE7cDEefBA9D5dDed319eC', 'stake': 8.724342855097579, 'provider': 'ollama', 'model': 'llama2', 'config': {'seed': 567438, 'stop': '', 'top_p': 0.78, 'num_gpu': 4}, 'updated_at': '06/17/2024, 21:47:04'}]...",
  "Leader {'id': 2, 'address': '0xBfE0B24B9C86D54384BAdC0426C7A7BDe7f71DFA', 'stake': 1.6300447758707397, 'provider': 'openai', 'model': 'gpt-4o-mini', 'config': {}, 'updated_at': '06/17/2024, 21:47:04'} starts contract execution...",
  "Leader {'id': 2, 'address': '0xBfE0B24B9C86D54384BAdC0426C7A7BDe7f71DFA', 'stake': 1.6300447758707397, 'provider': 'openai', 'model': 'gpt-4o-mini', 'config': {}, 'updated_at': '06/17/2024, 21:47:04'} has finished contract execution...",
  'Transaction has been fully executed...',
  "This is the data produced by the leader:\n\n {'vote': 'agree', 'result': {'args': ['test'], 'class': 'Storage', 'contract_state': 'gASVMAAAAAAAAACMCF9fbWFpbl9flIwHU3RvcmFnZZSTlCmBlH2UjAdzdG9yYWdllIwEdGVzdJRzYi4=', 'eq_outputs': {'leader': {}}, 'gas_used': 0, 'method': 'update_storage', 'mode': 'leader', 'node_config': {'address': '0xBfE0B24B9C86D54384BAdC0426C7A7BDe7f71DFA', 'config': {}, 'id': 2, 'model': 'gpt-4o-mini', 'provider': 'openai', 'stake': 1.6300447758707397, 'type': 'leader', 'updated_at': '06/17/2024, 21:47:04'}}}",
  'Transaction ID:\n\n None',
  {
    function: 'call_contract_function',
    trace_id: 'ljpjjd852',
    response: {
      status: 'info',
      message: 'db closed',
      data: {},
    },
  },
  {
    function: 'call_contract_function',
    trace_id: 'ljpjjd852',
    response: {
      status: 'success',
      message: '',
      data: {
        execution_output: {
          leader_data: {
            vote: 'agree',
            result: {
              args: ['test'],
              class: 'Storage',
              contract_state:
                'gASVMAAAAAAAAACMCF9fbWFpbl9flIwHU3RvcmFnZZSTlCmBlH2UjAdzdG9yYWdllIwEdGVzdJRzYi4=',
              eq_outputs: {
                leader: {},
              },
              gas_used: 0,
              method: 'update_storage',
              mode: 'leader',
              node_config: {
                address: '0xBfE0B24B9C86D54384BAdC0426C7A7BDe7f71DFA',
                config: {},
                id: 2,
                model: 'gpt-4o-mini',
                provider: 'openai',
                stake: 1.6300447758707397,
                type: 'leader',
                updated_at: '06/17/2024, 21:47:04',
              },
            },
          },
          consensus_data:
            '{"final":false,"votes":{"0xBfE0B24B9C86D54384BAdC0426C7A7BDe7f71DFA":"agree","0x1Da8FEfaD3d6A90F1BD49d03eCbb2E50aEB6C67A":"agree","0xbe109fB11baCa678DFCc3623296CAaf3a3E4cd6f":"agree","0xeD6EF403EC83b8Dd8feE7cDEefBA9D5dDed319eC":"agree"},"leader":{"vote":"agree","result":{"args":["test"],"class":"Storage","contract_state":"gASVMAAAAAAAAACMCF9fbWFpbl9flIwHU3RvcmFnZZSTlCmBlH2UjAdzdG9yYWdllIwEdGVzdJRzYi4=","eq_outputs":{"leader":{}},"gas_used":0,"method":"update_storage","mode":"leader","node_config":{"address":"0xBfE0B24B9C86D54384BAdC0426C7A7BDe7f71DFA","config":{},"id":2,"model":"gpt-4o-mini","provider":"openai","stake":1.6300447758707397,"type":"leader","updated_at":"06/17/2024, 21:47:04"}}},"validators":[{"vote":"agree","result":{"args":["test"],"class":"Storage","contract_state":"gASVMAAAAAAAAACMCF9fbWFpbl9flIwHU3RvcmFnZZSTlCmBlH2UjAdzdG9yYWdllIwEdGVzdJRzYi4=","eq_outputs":{"leader":{}},"gas_used":0,"method":"update_storage","mode":"validator","node_config":{"address":"0x1Da8FEfaD3d6A90F1BD49d03eCbb2E50aEB6C67A","config":{},"id":10,"model":"gpt-4o-mini","provider":"openai","stake":3.0603317919753037,"type":"validator","updated_at":"06/17/2024, 21:47:05"}}},{"vote":"agree","result":{"args":["test"],"class":"Storage","contract_state":"gASVMAAAAAAAAACMCF9fbWFpbl9flIwHU3RvcmFnZZSTlCmBlH2UjAdzdG9yYWdllIwEdGVzdJRzYi4=","eq_outputs":{"leader":{}},"gas_used":0,"method":"update_storage","mode":"validator","node_config":{"address":"0xbe109fB11baCa678DFCc3623296CAaf3a3E4cd6f","config":{"mirostat":1,"mirostat_tau":2.3,"num_gpu":1,"num_gqa":10,"num_thread":1,"repeat_penalty":1.5,"seed":961179,"stop":"","temprature":0.0,"tfs_z":1.9,"top_k":59},"id":6,"model":"llama2","provider":"ollama","stake":1.3238056014305584,"type":"validator","updated_at":"06/17/2024, 21:47:04"}}},{"vote":"agree","result":{"args":["test"],"class":"Storage","contract_state":"gASVMAAAAAAAAACMCF9fbWFpbl9flIwHU3RvcmFnZZSTlCmBlH2UjAdzdG9yYWdllIwEdGVzdJRzYi4=","eq_outputs":{"leader":{}},"gas_used":0,"method":"update_storage","mode":"validator","node_config":{"address":"0xeD6EF403EC83b8Dd8feE7cDEefBA9D5dDed319eC","config":{"num_gpu":4,"seed":567438,"stop":"","top_p":0.78},"id":7,"model":"llama2","provider":"ollama","stake":8.724342855097579,"type":"validator","updated_at":"06/17/2024, 21:47:04"}}}]}',
        },
      },
    },
  },
];

export const useTutorialStore = defineStore('tutorialStore', () => {
  const contractsStore = useContractsStore();
  const transactionsStore = useTransactionsStore();
  const nodeStore = useNodeStore();

  const resetTutorialState = () => {
    contractsStore.removeContractFile(mockContractId);
    contractsStore.removeDeployedContract(mockContractId);
    transactionsStore.transactions.forEach((t) => {
      if (t.localContractId === mockContractId) {
        transactionsStore.removeTransaction(t);
      }
    });
  };

  const addLog = async (message: any) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        nodeStore.logs.push({
          date: new Date().toISOString(),
          message,
        });
        resolve(0);
      }, 1500);
    });
  };

  async function addAndOpenContract() {
    const contractFile = {
      id: mockContractId,
      name: 'tutorial_storage.py',
      content: ((contractBlob as string) || '').trim(),
      example: true,
    };

    contractsStore.addContractFile(contractFile, true);
    contractsStore.openFile(mockContractId);
  }

  async function deployMockContract() {
    // For now we instantly mock the deployment of contract
    // In the future, we can improve this by properly mocking through the single contract store like for the schema
    // and thus preserve the appearance of async delays / loading times

    contractsStore.addDeployedContract(mockDeployedContract);

    nodeStore.logs.push({
      date: new Date().toISOString(),
      message: {
        function: 'deploy_intelligent_contract',
        trace_id: 'dstukqao9',
        response: { status: 'info', message: 'Starting...', data: {} },
      },
    });

    nodeStore.logs.push({
      date: new Date().toISOString(),
      message: {
        function: 'deploy_intelligent_contract',
        trace_id: 'dstukqao9',
        response: {
          status: 'success',
          message: '',
          data: {
            contract_id: '0x4Fb3673Ab7274ebBA6ff38EDB1ca5Bd0cd06C0FD',
          },
        },
      },
    });

    transactionsStore.addTransaction(mockDeploymentTx);

    return mockDeployedContract;
  }

  async function callContractMethod() {
    for (const log of contractFunctionLogs) {
      await addLog(log);
    }
    return new Promise((resolve) => {
      setTimeout(() => {
        transactionsStore.addTransaction({
          contractAddress: mockDeployedContract.address || '',
          localContractId: mockDeployedContract.contractId || '',
          txId: 100000,
          type: 'method',
          status: 'PENDING',
          data: {},
        });
        resolve(true);
      }, 2000);
    });
  }

  return {
    mockContractId,
    resetTutorialState,
    addAndOpenContract,
    deployMockContract,
    callContractMethod,
  };
});
