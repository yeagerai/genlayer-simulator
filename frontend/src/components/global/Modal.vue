<script setup>
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue';
import { XMarkIcon } from '@heroicons/vue/16/solid';
import { useUIStore } from '@/stores/ui';
import { watch } from 'vue';
const uiStore = useUIStore();

const props = defineProps({
  open: { type: Boolean, default: false },
  wide: { type: Boolean, default: false },
});

const emit = defineEmits(['close', 'onOpen']);

watch(
  () => props.open,
  (newVal) => {
    if (newVal) {
      emit('onOpen');
    }
  },
);
</script>

<template>
  <TransitionRoot as="template" :show="open">
    <Dialog
      class="relative z-20"
      @close="emit('close')"
      :data-mode="uiStore.mode"
    >
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div
          class="fixed inset-0 bg-zinc-900 bg-opacity-50 transition-opacity"
        />
      </TransitionChild>

      <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div
          class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
        >
          <TransitionChild
            as="template"
            enter="ease-out duration-150"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-100"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              class="relative transform overflow-hidden rounded-lg bg-gray-50 px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:p-6 dark:bg-zinc-700"
              :class="[!wide && 'sm:max-w-sm', wide && 'sm:max-w-xl']"
            >
              <GhostBtn @click="emit('close')" class="absolute right-3 top-3">
                <XMarkIcon class="h-5 w-5" />
              </GhostBtn>

              <div class="mt-4 flex flex-col gap-4">
                <div
                  v-if="$slots.icon"
                  class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100"
                >
                  <slot name="icon" />
                </div>

                <DialogTitle
                  v-if="$slots.title"
                  as="h3"
                  class="text-center text-xl font-semibold leading-6"
                >
                  <slot name="title" />
                </DialogTitle>

                <div v-if="$slots.description">
                  <p
                    class="text-center text-sm text-gray-600 dark:text-gray-300"
                  >
                    <slot name="description" />
                  </p>
                </div>

                <div v-if="$slots.info">
                  <div class="flex justify-center">
                    <div
                      class="rounded-md bg-gray-100 p-2 text-center font-semibold text-gray-600 dark:bg-gray-600 dark:text-white"
                    >
                      <slot name="info" />
                    </div>
                  </div>
                </div>

                <slot />
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
