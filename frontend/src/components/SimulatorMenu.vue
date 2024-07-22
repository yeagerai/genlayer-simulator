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
import SimulatorMenuLink from './SimulatorMenuLink.vue'
</script>

<template>
  <nav
    class="flex flex-col h-full items-center w-12 justify-between border-r dark:border-r-zinc-700 dark:bg-zinc-800 dark:text-white text-primary">
    <div class="flex flex-col items-center">
      <SimulatorMenuItem id="tutorial-how-to-change-example" :to="{ name: 'contracts' }" tooltip="Contracts"
        >
        <DocumentIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem id="tutorial-how-to-deploy" :to="{ name: 'run-debug' }" tooltip="Run and Debug">
        <CommandLineIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem :to="{ name: 'settings' }" tooltip="Settings">
        <AdjustmentsHorizontalIcon />
      </SimulatorMenuItem>
    </div>

    <div class="flex flex-col items-center">
      <SimulatorMenuLink :href="LINKS.docs" tooltip="GenLayer Docs">
        <DocumentTextIcon />
      </SimulatorMenuLink>

      <SimulatorMenuLink :href="LINKS.discord" tooltip="Discord">
        <DiscordIcon />
      </SimulatorMenuLink>

      <SimulatorMenuLink :href="LINKS.feedbackForm" tooltip="Feedback form">
        <HandThumbUpIcon />
      </SimulatorMenuLink>

      <SimulatorMenuItem :to="{ name: 'profile' }" tooltip="Profile">
        <UserCircleIcon />
      </SimulatorMenuItem>
    </div>
  </nav>
</template>
