import { describe, it, expect, beforeEach, vi, type Mock } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useTransactionsStore } from '@/stores';
import { useRpcClient } from '@/hooks';
import { type TransactionItem } from '@/types';

vi.mock('@/hooks', () => ({
  useRpcClient: vi.fn(),
}));

const testTransaction: TransactionItem = {
  hash: '0x1234567890123456789012345678901234567890',
  type: 'deploy',
  status: 'PENDING',
  contractAddress: '0xAf4ec2548dBBdc43ab6dCFbD4EdcEedde3FEAFB5',
  localContractId: '47490604-6ee9-4c0e-bf31-05d33197eedd',
};

const updatedTransactionPayload = {
  ...testTransaction,
  status: 'FINALIZED',
};

describe('useTransactionsStore', () => {
  let transactionsStore: ReturnType<typeof useTransactionsStore>;
  const mockRpcClient = {
    getTransactionByHash: vi.fn(),
  };

  beforeEach(() => {
    setActivePinia(createPinia());
    (useRpcClient as Mock).mockReturnValue(mockRpcClient);
    transactionsStore = useTransactionsStore();
    transactionsStore.transactions = [];
    transactionsStore.processingQueue = [];
    mockRpcClient.getTransactionByHash.mockClear();
  });

  it('should add a transaction', () => {
    transactionsStore.addTransaction(testTransaction);
    expect(transactionsStore.transactions).to.deep.include(testTransaction);
  });

  it('should remove an added transaction', () => {
    transactionsStore.addTransaction(testTransaction);
    expect(transactionsStore.transactions).to.deep.include(testTransaction);
    transactionsStore.removeTransaction(testTransaction);
    expect(transactionsStore.transactions).not.to.deep.include(testTransaction);
  });

  it('should update a transaction', () => {
    transactionsStore.addTransaction(testTransaction);
    transactionsStore.updateTransaction(updatedTransactionPayload);
    expect(transactionsStore.transactions[0].status).toBe('FINALIZED');
  });

  it('should get a transaction by hash using rpcClient', async () => {
    const transactionHash = '0x1234567890123456789012345678901234567890';
    const transactionData = { id: transactionHash, status: 'PENDING' };
    mockRpcClient.getTransactionByHash.mockResolvedValue(transactionData);

    const result = await transactionsStore.getTransaction(transactionHash);

    expect(mockRpcClient.getTransactionByHash).toHaveBeenCalledWith(
      transactionHash,
    );
    expect(result).toEqual(transactionData);
  });

  it('should clear transactions for a specific contract', () => {
    const tx1 = {
      ...testTransaction,
      hash: '0x1234567890123456789012345678901234567891',
      localContractId: 'contract-1',
    };
    const tx2 = {
      ...testTransaction,
      hash: '0x1234567890123456789012345678901234567892',
      localContractId: 'contract-2',
    };

    transactionsStore.addTransaction(tx1);
    transactionsStore.addTransaction(tx2);

    transactionsStore.processingQueue = [tx1];

    transactionsStore.clearTransactionsForContract('contract-1');

    expect(transactionsStore.transactions).toEqual([tx2]);
    expect(transactionsStore.processingQueue).toEqual([]);
  });

  it('should compute pending transactions', () => {
    const tx1 = {
      ...testTransaction,
      hash: '0x1234567890123456789012345678901234567891',
      status: 'FINALIZED',
    };
    const tx2 = {
      ...testTransaction,
      hash: '0x1234567890123456789012345678901234567892',
      status: 'PENDING',
    };

    transactionsStore.transactions = [tx1, tx2];

    expect(transactionsStore.pendingTransactions).toEqual([tx2]);
  });
});
