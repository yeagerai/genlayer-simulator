<script setup lang="ts">
import {
  DocumentIcon,
  Cog6ToothIcon,
  CommandLineIcon,
  HandThumbUpIcon,
  DocumentTextIcon,
  ServerIcon,
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
        :to="{ name: 'contracts' }"
        v-tooltip="{ content: 'Contracts', placement: 'right' }"
      >
        <DocumentIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem
        :to="{ name: 'run-debug' }"
        v-tooltip="{ content: 'Run and Debug', placement: 'right' }"
      >
        <CommandLineIcon />
      </SimulatorMenuItem>

      <SimulatorMenuItem
        :to="{ name: 'validators' }"
        v-tooltip="{ content: 'Validators', placement: 'right' }"
      >
        <ServerIcon />
      </SimulatorMenuItem>
    </div>

    <div class="flex flex-col items-center">
      <SimulatorMenuLink
        :href="LINKS.docs"
        v-tooltip="{ content: 'GenLayer Docs', placement: 'right' }"
      >
        <DocumentTextIcon />
      </SimulatorMenuLink>

      <SimulatorMenuLink
        :href="LINKS.discord"
        v-tooltip="{ content: 'Discord', placement: 'right' }"
      >
        <DiscordIcon />
      </SimulatorMenuLink>

      <SimulatorMenuLink
        :href="LINKS.feedbackForm"
        v-tooltip="{ content: 'Feedback Form', placement: 'right' }"
      >
        <HandThumbUpIcon />
      </SimulatorMenuLink>

      <SimulatorMenuItem
        :to="{ name: 'settings' }"
        v-tooltip="{ content: 'Settings', placement: 'right' }"
      >
        <Cog6ToothIcon />
      </SimulatorMenuItem>
    </div>
  </nav>
</template>
