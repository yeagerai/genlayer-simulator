import type { ContractFile, Address } from '@/types';
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { notify } from '@kyvg/vue3-notification';
import { useDb, useFileName, useSetupStores } from '@/hooks';
import { v4 as uuidv4 } from 'uuid';

// TODO: challenge contractFile vs id -> normalize? use middleware?
export const useContractsStore = defineStore(
  'contractsStore',
  () => {
    const contracts = ref<ContractFile[]>([]);
    const db = useDb();
    // const { setupStores } = useSetupStores();
    const { cleanupFileName } = useFileName();

    const currentContractId = ref<string>('');

    function addContractFile(contract: ContractFile): void {
      const name = cleanupFileName(contract.name);
      contracts.value.push({ ...contract, name });
    }

    function checkOpenTabs() {
      console.log('checkOpenTabs', currentContractId.value);
      // TODO: triple check this logic
      const currentlyOpenContract = contracts.value.find(
        (c) => c.id === currentContractId.value && c.isOpened,
      );

      if (currentlyOpenContract) {
        console.log('stop');

        return;
      }

      const anyOpenFile = contracts.value.find((c) => c.isOpened);

      if (anyOpenFile) {
        console.log('anyOpenFile');

        focusFile(anyOpenFile.id);
      } else {
        console.log('fallback to home tab');

        setCurrentContractId('');
      }
    }

    function removeContractFile(id: string): void {
      contracts.value = contracts.value.filter((c) => c.id !== id);
      checkOpenTabs();
    }

    // TODO: could use the interface for the second argument as well
    function updateContractFile(
      id: string,
      { name, content }: { name?: string; content?: string },
    ) {
      const contract = contracts.value.find((c) => c.id === id);

      if (!contract) {
        return;
      }

      if (name) {
        contract.name = cleanupFileName(contract.name);
      }

      if (content) {
        contract.content = content;
      }

      if (name || content) {
        contract.updatedAt = new Date().toISOString();
      }
    }

    function openFile(id: string) {
      const contract = contracts.value.find((c) => c.id === id);

      if (contract) {
        contract.isOpened = true;
        focusFile(contract.id);
      }
    }

    function focusFile(id: string) {
      console.log('focusFile', id);
      setCurrentContractId(id);
    }

    function closeFile(id: string) {
      const contract = contracts.value.find((c) => c.id === id);

      if (contract) {
        contract.isOpened = false;
        checkOpenTabs();
      }
    }

    function setContractAsDeployed(
      id: string,
      {
        address,
        defaultState,
      }: {
        address: Address;
        defaultState: string;
      },
    ): void {
      const contract = contracts.value.find((c) => c.id === id);

      if (!contract) {
        return;
      }

      contract.address = address;
      contract.defaultState = defaultState;

      notify({
        title: 'Contract deployed',
        type: 'success',
      });
    }

    function setCurrentContractId(id?: string) {
      console.trace('setCurrentContractId', id);
      currentContractId.value = id || '';
    }

    async function loadExampleContracts() {
      const contractsBlob = import.meta.glob(
        '@/assets/examples/contracts/*.py',
        {
          query: '?raw',
          import: 'default',
        },
      );

      for (const key of Object.keys(contractsBlob)) {
        const raw = await contractsBlob[key]();
        const name = key.split('/').pop() || 'ExampleContract.py';

        if (!contracts.value.some((c) => c.name === name)) {
          const contract = {
            id: uuidv4(),
            name,
            content: ((raw as string) || '').trim(),
            example: true,
          };

          addContractFile(contract);
        }
      }
    }

    async function resetStorage(): Promise<void> {
      // TODO: Re-implement a proper reset
      contracts.value = [];
      setCurrentContractId('');
      await loadExampleContracts();
    }

    // Getters

    const currentContract = computed(() => {
      return contracts.value.find((c) => c.id === currentContractId.value);
    });

    const contractsOrderedByName = computed(() => {
      return contracts.value
        .slice()
        .sort((a, b) => a.name.localeCompare(b.name));
    });

    const openedFiles = computed(() => {
      return contracts.value.filter((c) => c.isOpened);
    });

    const deployedContracts = computed(() => {
      return contracts.value.filter((c) => c.address);
    });

    return {
      // state
      contracts,
      currentContractId,

      // getters
      currentContract,
      openedFiles,
      deployedContracts,
      contractsOrderedByName,

      // actions
      addContractFile,
      removeContractFile,
      updateContractFile,
      openFile,
      closeFile,
      setContractAsDeployed,
      setCurrentContractId,
      resetStorage,
    };
  },
  {
    persist: {
      paths: ['currentContractId'],
    },
  },
);
