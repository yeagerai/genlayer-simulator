<script lang="ts" setup>
import VerticalNavGroup from '@layouts/components/VerticalNavGroup.vue'
import VerticalNavLink from '@layouts/components/VerticalNavLink.vue'
import VerticalNavSectionTitle from '@/@layouts/components/VerticalNavSectionTitle.vue'
</script>

<template>
  <VerticalNavLink
    :item="{
      title: 'Getting Started',
      icon: 'ri-home-smile-line',
      to: '/getting-started'
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Accounts',
      icon: 'ri-table-alt-line',
      to: '/accounts'
    }"
  />
  <VerticalNavLink
    :item="{
      title: 'Settings',
      icon: 'ri-settings-line',
      to: '/settings'
    }"
  />
</template>
