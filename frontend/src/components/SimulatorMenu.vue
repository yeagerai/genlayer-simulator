<script setup lang="ts">
import {
  DocumentIcon,
  AdjustmentsHorizontalIcon,
  UserCircleIcon,
  CommandLineIcon,
  HandThumbUpIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/solid'
import DiscordIcon from '@/assets/icons/DiscordIcon.vue'
import { LINKS } from '@/constants/links'
import SimulatorMenuItem from './SimulatorMenuItem.vue'
</script>

<template>
  <nav
    class="flex flex-col h-full items-center w-12 justify-between border-r dark:border-r-zinc-700 dark:bg-zinc-800 dark:text-white text-primary">
    <div class="flex flex-col items-center">
      <SimulatorMenuItem id="tutorial-how-to-change-example" :to="{ name: 'simulator.contracts' }" tooltip="Contracts"
        class="link-contracts">
        <DocumentIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem id="tutorial-how-to-deploy" :to="{ name: 'simulator.run-debug' }" tooltip="Run and Debug">
        <CommandLineIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem :to="{ name: 'simulator.settings' }" tooltip="Settings">
        <AdjustmentsHorizontalIcon />
      </SimulatorMenuItem>
    </div>

    <div class="flex flex-col items-center">
      <SimulatorMenuItem :href="LINKS.docs" tooltip="GenLayer Docs" class="link-docs">
        <DocumentTextIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem :href="LINKS.discord" tooltip="Discord">
        <DiscordIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem :href="LINKS.feedbackForm" tooltip="Feedback form">
        <HandThumbUpIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem :to="{ name: 'profile' }" tooltip="Profile">
        <UserCircleIcon />
      </SimulatorMenuItem>
    </div>
  </nav>
</template>
