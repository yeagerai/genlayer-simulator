<script setup lang="ts">
import { useContractsStore } from '@/stores';
import { computed } from 'vue';
import HomeContractItem from '@/components/Simulator/HomeContractItem.vue';
import { LINKS } from '@/constants/links';
import { DocumentPlusIcon, DocumentTextIcon } from '@heroicons/vue/24/solid';

const contractStore = useContractsStore();

const storageContract = computed(() => {
  return contractStore.contracts.find(
    (contract) => contract.name === 'storage.gpy',
  );
});

const wizardOfCoinContract = computed(() => {
  return contractStore.contracts.find(
    (contract) => contract.name === 'wizard_of_coin.gpy',
  );
});

const llmERC20Contract = computed(() => {
  return contractStore.contracts.find(
    (contract) => contract.name === 'llm_erc20.gpy',
  );
});

const hasAnySampleContract = computed(() => {
  return (
    storageContract.value ||
    wizardOfCoinContract.value ||
    llmERC20Contract.value
  );
});
</script>

<template>
  <div class="h-full w-full overflow-y-auto @container">
    <div
      class="mx-auto flex h-full max-w-[1200px] flex-col gap-4 p-4 @[1024px]:flex-row @[1024px]:gap-8"
    >
      <div class="grid place-content-center">
        <div class="rounded-md bg-slate-600 bg-opacity-10 p-4 @[1024px]:p-8">
          <h1 class="mb-4 text-lg font-semibold">
            Welcome to the GenLayer Simulator
          </h1>

          <div class="text-sm">
            <p class="my-2">
              Genlayer is a blockchain that has AI-powered smart contracts that
              can natively connect to the internet and understand code and
              natural language.
            </p>
            <p class="my-2">
              This Simulator is an interactive sandbox designed for developers
              to explore the potential of GenLayer’s Intelligent Contracts. It
              replicates the GenLayer network’s execution environment and
              consensus algorithm, but offers a controlled and local environment
              to test different ideas and behaviors.
            </p>
          </div>

          <h2 class="my-4 font-semibold">
            What you can do with the GenLayer Simulator
          </h2>

          <ul class="flex list-disc flex-col gap-2 pl-4 text-sm">
            <li>
              <b>Experiment with AI smart contracts:</b> Intelligent Contracts
              leverage LLMs, such as
              <a href="https://openai.com/research/gpt-4" target="_blank"
                >GPT-4</a
              >
              or
              <a href="https://llama.meta.com/llama3" target="_blank">Llama3</a
              >, to understand natural language and be capable of complex
              decision making.
            </li>
            <li>
              <b>Access the Internet:</b> Genlayer is the first platform where
              smart contracts don't need oracles to access the Internet.
            </li>
            <li>
              <b>Code in Python:</b> Develop in a familiar, developer-friendly
              language, where memory and string management are not a big
              headache.
            </li>
          </ul>

          <div class="text-sm">
            <p class="my-2">
              Currently, the Simulator does not support token transfers,
              contract-to-contract interactions, or gas consumption. These
              features will be added as the platform evolves.
            </p>
            <p class="my-2">
              <a :href="LINKS.feedbackForm" target="_blank" class="underline"
                >Your feedback</a
              >
              and contributions are crucial in shaping GenLayer. Together we can
              create the next generation of AI-powered Smart Contracts!
            </p>
            <div class="mt-4 flex flex-row items-center gap-2">
              <a :href="LINKS.docs" target="_blank">
                <Btn secondary>
                  <DocumentTextIcon class="h-4 w-4" />
                  View Docs</Btn
                >
              </a>
              <!-- <Btn primary>
                <DocumentPlusIcon class="h-4 w-4" />
                New Contract</Btn
              > -->
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="hasAnySampleContract"
        class="grid min-w-[300px] place-content-center gap-2"
      >
        <h2 class="font-semibold">Intelligent Contract Templates</h2>

        <div
          class="grid grid-cols-1 gap-2 pb-4 @[800px]:grid-cols-3 @[1024px]:grid-cols-1 @[1024px]:pb-0"
        >
          <HomeContractItem
            v-if="storageContract"
            :contract="storageContract"
            title="Simple Storage"
          >
            Cover the basics of Intelligent Contracts. Learn how to store,
            retrieve, and update data.
          </HomeContractItem>

          <HomeContractItem
            v-if="wizardOfCoinContract"
            :contract="wizardOfCoinContract"
            title="Wizard of Coin"
          >
            Test your wit to see and convince the wizard to hand over the coin.
            Learn how Intelligent Contracts can manage interactions and asset
            control.
          </HomeContractItem>

          <HomeContractItem
            v-if="llmERC20Contract"
            :contract="llmERC20Contract"
            title="LLM ERC20"
          >
            Re-create the ERC20 standard and handle ownership of tokens using
            natural language.
          </HomeContractItem>
        </div>
      </div>
    </div>
  </div>
</template>
