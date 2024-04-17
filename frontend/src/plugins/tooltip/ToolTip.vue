<script setup>
import tippy from "tippy.js";
import "tippy.js/dist/tippy.css";
import { onMounted, ref, onUpdated, onUnmounted, inject } from "vue";
import { tooltipOptionsInject } from "./";
const props = defineProps({
  text: { type: String, required: true },
  options: {
    type: Object,
    default() {
      return {};
    },
  },
});

const tooltip = ref(null);

let tippyInstance = null;

function initTippy() {
  if (tippyInstance) tippyInstance.destroy();
  tippyInstance = tippy(tooltip.value.parentNode, {
    ...inject(tooltipOptionsInject),
    content: props.text,
    ...props.options,
  });
}
onMounted(initTippy);
onUpdated(initTippy);
onUnmounted(() => tippyInstance.destroy());
</script>
<template>
  <span ref="tooltip"></span>
</template>