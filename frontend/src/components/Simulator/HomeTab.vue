<script setup lang="ts"></script>
<template>
  <div class="flex overflow-y-auto px-6 py-2">
    <div class="flex">
      <div class="flex w-full flex-col md:w-3/5">
        <div class="flex flex-col">
          <div class="mt-4 flex">
            <h1 class="text-2xl">Welcome to the GenLayer Simulator</h1>
          </div>
          <div class="flex flex-col pt-2">
            <p class="pb-3">
              Genlayer is a blockchain that has AI-powered smart contracts that can natively connect
              to the internet and understand code and natural language.
            </p>
            <p class="pb-3">
              This Simulator is an interactive sandbox designed for developers to explore the
              potential of GenLayer’s Intelligent Contracts. It replicates the GenLayer network’s
              execution environment and consensus algorithm, but offers a controlled and local
              environment to test different ideas and behaviors.
            </p>
          </div>
        </div>
        <div class="flex flex-col">
          <div class="mt-4 flex">
            <h1 class="text-2xl">What you can do with the GenLayer Simulator:</h1>
          </div>
          <div class="flex flex-col pt-2">
            <ul>
              <li>
                <b>Experiment with AI smart contracts:</b> Intelligent Contracts leverage LLMs, such
                as
                <a
                  href="https://openai.com/research/gpt-4"
                  target="_blank"
                  class="font-semibold text-primary underline dark:text-white"
                >
                  GPT-4
                </a>
                or
                <a
                  href="https://llama.meta.com/llama3"
                  target="_blank"
                  class="font-semibold text-primary underline dark:text-white"
                >
                  Llama3 </a
                >, to understand natural language and be capable of complex decision making.
              </li>
              <li>
                <b>Internet Access:</b> Genlayer is the first platform where smart contracts don't
                need oracles to access the internet.
              </li>

              <li>
                <b>Code in Python:</b> Develop in a familiar, developer-friendly language, where
                memory and string management are not a big headache.
              </li>
            </ul>
          </div>
          <div class="flex flex-col pt-2">
            <p class="pb-3">
              Currently, the Simulator does not support token transfers, contract-to-contract
              interactions, or gas consumption. These features will be added as the platform
              evolves.
            </p>
            <p class="pb-3">
              Your feedback and contributions are crucial in shaping GenLayer. Together we can
              create the next generation of AI-powered Smart Contracts!
            </p>
            <p>
              To get started, explore the following resources:
              <a
                href="https://genlayer-docs.netlify.app/"
                target="_blank"
                class="font-semibold text-primary underline dark:text-white"
              >
                GenLayer Docs
              </a>
            </p>
          </div>
        </div>
      </div>
      <div class="flex h-full w-full flex-col md:ml-6 md:w-2/5">
        <div class="mb-2 mt-4 flex">
          <h2 class="text-xl">Intelligent Contracts Templates</h2>
        </div>
        <div class="flex flex-col rounded-md bg-slate-400 p-6 dark:bg-slate-600">
          <div class="m-2 flex flex-col rounded-md bg-slate-100 p-6 dark:bg-slate-500">
            <div class="flex">
              <h4 class="text-md font-semibold">Wizard of Coin</h4>
            </div>
            <div class="mt-1 text-justify text-sm">
              Dive into the <b>"Wizard of Coin"</b> template that allows you to interact with a
              magical world. In this scenario, you meet a wizard who guards a highly sought-after
              coin. Test your skills and strategy to see if you can convince the wizard to hand over
              the coin. This template is perfect for learning how Intelligent Contracts can manage
              interactions and asset control in a fun and engaging way.
            </div>
          </div>
          <div class="m-2 flex flex-col rounded-md bg-slate-100 p-6 dark:bg-slate-500">
            <div class="flex">
              <h4 class="text-md font-semibold">Simple Storage</h4>
            </div>
            <div class="mt-1 text-justify text-sm">
              Explore the <b>"Simple Storage"</b> template to understand the basics of Intelligent
              Contracts. This template offers a straightforward platform where you can store,
              retrieve, and update data. It's an excellent starting point for anyone new to
              blockchain technology, demonstrating how simple it is to interact with a decentralized
              database using Intelligent Contracts.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
