<template>
  <div class="h-100 d-flex align-center justify-space-between">
    <!-- 👉 Footer: left content -->
    <span class="d-flex align-center">
      &copy;
      {{ new Date().getFullYear() }}
      <a
        href="https://genlayer.com"
        target="_blank"
        rel="noopener noreferrer"
        class="text-primary ms-1"
        >GenLayer</a
      >
    </span>
    <!-- 👉 Footer: right content -->
    <span class="d-md-flex gap-x-4 text-primary d-none" />
  </div>
</template>
