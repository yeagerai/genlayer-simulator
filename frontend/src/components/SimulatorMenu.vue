<script setup lang="ts">
import {
  DocumentIcon,
  Cog6ToothIcon,
  UserCircleIcon,
  CommandLineIcon,
  HandThumbUpIcon,
  DocumentTextIcon,
} from '@heroicons/vue/24/solid';
import DiscordIcon from '@/assets/icons/DiscordIcon.vue';
import { LINKS } from '@/constants/links';
import SimulatorMenuItem from './SimulatorMenuItem.vue';
import SimulatorMenuLink from './SimulatorMenuLink.vue';
</script>

<template>
  <nav
    class="flex h-full w-12 flex-col items-center justify-between border-r text-primary dark:border-r-zinc-700 dark:bg-zinc-800 dark:text-white"
  >
    <div class="flex flex-col items-center">
      <SimulatorMenuItem
        id="tutorial-how-to-change-example"
        :to="{ name: 'contracts' }"
        tooltip="Contracts"
      >
        <DocumentIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem
        id="tutorial-how-to-deploy"
        :to="{ name: 'run-debug' }"
        v-tooltip="'Run and Debug'"
      >
        <CommandLineIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem :to="{ name: 'settings' }" tooltip="Settings">
        <Cog6ToothIcon />
      </SimulatorMenuItem>
    </div>

    <div class="flex flex-col items-center">
      <SimulatorMenuLink :href="LINKS.docs" v-tooltip="'GenLayer Docs'">
        <DocumentTextIcon />
      </SimulatorMenuLink>

      <SimulatorMenuLink :href="LINKS.discord" v-tooltip="'Discord'">
        <DiscordIcon />
      </SimulatorMenuLink>

      <SimulatorMenuLink :href="LINKS.feedbackForm" v-tooltip="'Feedback form'">
        <HandThumbUpIcon />
      </SimulatorMenuLink>

      <SimulatorMenuItem :to="{ name: 'profile' }" v-tooltip="'Profile'">
        <UserCircleIcon />
      </SimulatorMenuItem>
    </div>
  </nav>
</template>
