import { describe, it, expect, beforeEach, vi, type Mock } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useTransactionsStore } from '@/stores';
import { useRpcClient } from '@/hooks';
import { type TransactionItem } from '@/types';

vi.mock('@/hooks', () => ({
  useRpcClient: vi.fn(),
}));

const testTransaction: TransactionItem = {
  type: 'deploy',
  status: 'PENDING',
  contractAddress: '0xAf4ec2548dBBdc43ab6dCFbD4EdcEedde3FEAFB5',
  localContractId: '47490604-6ee9-4c0e-bf31-05d33197eedd',
  txId: 140,
};

const updatedTransactionPayload = {
  id: 140,
  type: 'deploy',
  status: 'FINALIZED',
  contractAddress: '0xAf4ec2548dBBdc43ab6dCFbD4EdcEedde3FEAFB5',
  localContractId: '47490604-6ee9-4c0e-bf31-05d33197eedd',
};

describe('useTransactionsStore', () => {
  let transactionsStore: ReturnType<typeof useTransactionsStore>;
  const mockRpcClient = {
    getTransactionById: vi.fn(),
  };

  beforeEach(() => {
    setActivePinia(createPinia());
    (useRpcClient as Mock).mockReturnValue(mockRpcClient);
    transactionsStore = useTransactionsStore();
    transactionsStore.transactions = [];
    transactionsStore.processingQueue = [];
    mockRpcClient.getTransactionById.mockClear();
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

  it('should get a transaction by id using rpcClient', async () => {
    const transactionId = 123;
    const transactionData = { id: transactionId, status: 'PENDING' };
    mockRpcClient.getTransactionById.mockResolvedValue(transactionData);

    const result = await transactionsStore.getTransaction(transactionId);

    expect(mockRpcClient.getTransactionById).toHaveBeenCalledWith(
      transactionId,
    );
    expect(result).toEqual(transactionData);
  });

  it('should clear transactions for a specific contract', () => {
    const tx1 = { ...testTransaction, txId: 1, localContractId: 'contract-1' };
    const tx2 = { ...testTransaction, txId: 2, localContractId: 'contract-2' };

    transactionsStore.addTransaction(tx1);
    transactionsStore.addTransaction(tx2);

    transactionsStore.processingQueue = [tx1];

    transactionsStore.clearTransactionsForContract('contract-1');

    expect(transactionsStore.transactions).toEqual([tx2]);
    expect(transactionsStore.processingQueue).toEqual([]);
  });

  it('should compute pending transactions', () => {
    const tx1 = { ...testTransaction, txId: 1, status: 'FINALIZED' };
    const tx2 = { ...testTransaction, txId: 2, status: 'PENDING' };

    transactionsStore.transactions = [tx1, tx2];

    expect(transactionsStore.pendingTransactions).toEqual([tx2]);
  });
});
