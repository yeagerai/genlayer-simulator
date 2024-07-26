<template>
  <div
    class="flex w-full flex-row items-center justify-between bg-slate-100 p-2 dark:dark:bg-zinc-700"
  >
    <h4 class="text-md">
      <slot name="title" />
    </h4>

    <slot name="actions" />
  </div>

  <div class="flex w-full flex-col p-2 gap-2">
    <slot />
  </div>
</template>
