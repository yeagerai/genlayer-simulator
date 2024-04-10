<script setup lang="ts">
import { onMounted } from "vue";
import { watchEffect } from "vue";
import { watch } from "vue";
import { onUnmounted } from "vue";
import { ref } from "vue";
import { useGoTo } from 'vuetify'
import { VVirtualScroll } from "vuetify/components";
import { webSocketClient } from "@/utils";

const logs = ref<{ message: string, date: string }[]>([])
const virtualScroll = ref<VVirtualScroll>()
const scrollContainer = ref<Element>()
const goTo = useGoTo()
onMounted(() => {
  webSocketClient.on("status_update", (event) => {
    console.log('webSocketClient.details', event)
    logs.value.push({ date: (new Date()).toISOString(), message: event.message })
  });
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
  if (webSocketClient.connected) {
    webSocketClient.close()
  }
})
</script>
<template>
  <v-card>
    <v-toolbar density="compact">
      <v-toolbar-title>Node Logs</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <div class="logs-container">
      <v-virtual-scroll :items="logs" ref="virtualScroll">
        <template v-slot:default="{ item, index }">
          <v-list-item density="compact" class="item" :id="`log-item-${index}`">
            <template v-slot:prepend>
              <div class="mr-3 logs-line-number">{{ index + 1 }}</div>
            </template>
            <template v-slot:append>
            </template>
            <v-list-item-subtitle class="subtitle">
              <small>{{ item.date }}</small> :: {{ item.message }}
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
