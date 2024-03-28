<script setup lang="ts">
import { onMounted } from "vue";
import { watchEffect } from "vue";
import { watch } from "vue";
import { onUnmounted } from "vue";
import { ref } from "vue";
import { useGoTo } from 'vuetify'
import { VVirtualScroll } from "vuetify/components";
const items = [
  'INFO [09-06|01:31:59.910] Submitted transaction             hash=0x2893b70483bf1791b550e5a93763058b0abf7c6d9e6201e07212dbc64d4764532 from: 0xFB48587362536C606d6e89f717Fsd229673246e6 nonce: 43 recipient: 0x7C60662d63536e89f717F9673sd22246F6eB4858 value: 100,000,000,000,000,000',
  'WARN [10-03|18:00:40.413] Unexpected trienode heal packet          peer=9f0e8fbf         reqid=6,915,308,639,612,522,441',
  'WARN [10-03 |13:10:26.499] Beacon client online, but never received consensus updates. Please ensure your beacon client is operational to follow the chain!',
  '# consensus client has identified a new head to use as a sync target - account for this in state sync',
  'WARN [09-28|11:06:01.363] Snapshot extension registration failed'
]
let historyInterval: NodeJS.Timeout;
const logs = ref<string[]>([])
const virtualScroll = ref<VVirtualScroll>()
const scrollContainer = ref<Element>()
const goTo = useGoTo()
onMounted(() => {
  historyInterval = setInterval(() => {
    const rand = Math.floor(Math.random() * (5 - 1) + 1)
    logs.value.push(items[rand] || 'Command...')

  }, 2000);
})
watch(logs.value, () => {

  if (!scrollContainer.value) {
    scrollContainer.value = virtualScroll.value?.$el.querySelector('.v-virtual-scroll__container')
  }
  const scrollTo = scrollContainer.value?.clientHeight || 400

  goTo(scrollTo, {
    container: virtualScroll.value?.$el,
    duration: 300,
    easing: 'easeInQuad',
    offset: 0
  })
})
onUnmounted(() => {
  if (historyInterval) {
    clearInterval(historyInterval)
  }
})
</script>
<template>
  <v-card>
    <v-toolbar density="compact">
      <v-toolbar-title>Node Logs</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <div class="flex mx-2 logs-container">
      <v-virtual-scroll :items="logs" ref="virtualScroll">
        <template v-slot:default="{ item, index }">
          <v-list-item density="compact" class="item" :id="`log-item-${index}`">
            <template v-slot:prepend>
              <div class="mr-3 logs-line-number">{{ index + 1 }}</div>
            </template>
            <template v-slot:append>
            </template>
            <v-list-item-subtitle class="subtitle">
              {{ item }}
            </v-list-item-subtitle>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </div>

  </v-card>
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
  display: flex;
  height: 25rem;
  background-color: #333333;
  font-family: monospace;
  color: #f2f2f2;
  min-height: 20rem !important;
}

.subtitle {
  font-size: 0.8rem;
}
</style>
