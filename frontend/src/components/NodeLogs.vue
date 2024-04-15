<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch, watchEffect } from 'vue'
import { useGoTo } from 'vuetify'
import { VVirtualScroll } from 'vuetify/components'
import { webSocketClient } from '@/utils'

const logs = ref<{ message: string; date: string }[]>([])
const virtualScroll = ref<VVirtualScroll>()
const scrollContainer = ref<Element>()
const goTo = useGoTo()

onMounted(() => {
  webSocketClient.on('status_update', (event) => {
    console.log('webSocketClient.details', event)
    logs.value.push({ date: new Date().toISOString(), message: event.message })
  })
})

watch(logs.value, () => {
  if (!scrollContainer.value)
    scrollContainer.value = virtualScroll.value?.$el.querySelector('.v-virtual-scroll__container')

  const scrollTo = scrollContainer.value?.clientHeight || 400

  goTo(scrollTo, {
    container: virtualScroll.value?.$el,
    duration: 300,
    easing: 'easeInQuad',
    offset: 0
  })
})

onUnmounted(() => {
  if (webSocketClient.connected) webSocketClient.close()
})
</script>

<template>
  <VCard>
    <VToolbar density="compact">
      <VToolbarTitle>Node Logs</VToolbarTitle>
      <VSpacer />
    </VToolbar>
    <div class="logs-container">
      <VVirtualScroll ref="virtualScroll" :items="logs" :height="400">
        <template #default="{ item, index }">
          <VListItem :id="`log-item-${index}`" density="compact" class="item">
            <template #prepend>
              <div class="mr-3 logs-line-number">
                {{ index + 1 }}
              </div>
            </template>
            <template #append />
            <VListItemSubtitle class="subtitle">
              <small>{{ item.date }}</small> :: {{ item.message }}
            </VListItemSubtitle>
          </VListItem>
        </template>
      </VVirtualScroll>
    </div>
  </VCard>
</template>

<style>
.logs-line-number {
  font-size: 0.7rem;
}

.item {
  overflow: auto;
  width: 100% !important;
  display: flex;
}

.logs-container {
  height: 25rem;
  background-color: #333333;
  font-family: monospace;
  color: #f2f2f2;
  min-height: 20rem !important;
}

.subtitle {
  font-size: 0.7rem;
}
</style>
