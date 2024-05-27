<script setup lang="ts">
import { RouterLink } from 'vue-router'
import {
  DocumentIcon,
  AdjustmentsHorizontalIcon,
  UserCircleIcon,
  CommandLineIcon,
  HandThumbUpIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/solid'
import DiscordIcon from '@/assets/icons/DiscordIcon.vue'
</script>

<template>
  <nav
    class="flex flex-col h-full items-center w-12 justify-between border-r border-r-slate-300 dark:border-r-white/60 dark:bg-zinc-800 dark:text-white text-primary"
  >
    <div class="flex flex-col items-center">
      <RouterLink
        :to="{ name: 'simulator.contracts' }"
        id="tutorial-how-to-change-example"
        class="link-contracts p-3 border-r-4 border-transparent hover:border-r-primary hover:opacity-100"
      >
        <DocumentIcon class="h-6 w-6 dark:fill-white fill-primary" />
        <ToolTip text="Contracts" :options="{ placement: 'right' }" />
      </RouterLink>
      <RouterLink
        :to="{ name: 'simulator.run-debug' }"
        id="tutorial-how-to-deploy"
        class="p-3 border-r-4 border-transparent hover:border-r-primary hover:opacity-100"
      >
        <CommandLineIcon class="h-6 w-6 dark:fill-white fill-primary" />
        <ToolTip text="Run and Debug" :options="{ placement: 'right' }" />
      </RouterLink>
      <RouterLink
        :to="{ name: 'simulator.settings' }"
        class="p-3 border-r-4 border-transparent hover:border-r-primary hover:opacity-100"
      >
        <AdjustmentsHorizontalIcon class="h-6 w-6 dark:fill-white fill-primary" />
        <ToolTip text="Settings" :options="{ placement: 'right' }" />
      </RouterLink>
    </div>
    <div class="flex flex-col items-center">
      <a
        href="https://genlayer-docs.netlify.app/"
        target="_blank"
        class="link-docs p-3 border-r-4 border-transparent hover:border-r-primary hover:opacity-100"
      >
        <DocumentTextIcon class="h-6 w-6 dark:fill-white fill-primary" />
        <ToolTip text="GenLayer Docs" :options="{ placement: 'right' }" />
      </a>
      <a
        href="https://discord.gg/wNSBXcYmJP"
        target="_blank"
        class="p-3 border-r-4 border-transparent hover:border-r-primary hover:opacity-100"
      >
        <DiscordIcon class="h-6 w-6 dark:fill-white fill-primary" />
        <ToolTip text="Discord" :options="{ placement: 'right' }" />
      </a>
      <a
        href="https://docs.google.com/forms/d/1IVNsZwm936kSNCiXmlAP8bgJnbik7Bqaoc3I6UYhr-o/viewform?edit_requested=true"
        target="_blank"
        class="p-3 border-r-4 border-transparent hover:border-r-primary hover:opacity-100"
      >
        <HandThumbUpIcon class="h-6 w-6 dark:fill-white fill-primary" />
        <ToolTip text="Feedback form" :options="{ placement: 'right' }" />
      </a>
      <RouterLink
        :to="{ name: 'profile' }"
        class="p-3 border-r-4 border-transparent hover:border-r-primary hover:opacity-100"
      >
        <UserCircleIcon class="h-6 w-6 dark:fill-white fill-primary" />
        <ToolTip text="Profile" :options="{ placement: 'right' }" />
      </RouterLink>
    </div>
  </nav>
</template>

<style scoped></style>
