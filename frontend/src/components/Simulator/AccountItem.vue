<script setup lang="ts">
import { useAccountsStore } from '@/stores';
import { notify } from '@kyvg/vue3-notification';
import { TrashIcon } from '@heroicons/vue/24/solid';
import { PowerCircle } from 'lucide-vue-next';
import { ref } from 'vue';

const store = useAccountsStore();

const setCurentAddress = () => {
  store.setCurrentAccount(props.privateKey);
  notify({
    title: 'Active account changed',
    type: 'success',
  });
};

const deleteAddress = () => {
  store.removeAccount(props.privateKey);
  notify({
    title: 'Account deleted',
    type: 'success',
  });
  deleteModalOpen.value = false;
};

const props = defineProps<{
  active?: Boolean;
  privateKey: `0x${string}`;
  canDelete?: Boolean;
}>();

const deleteModalOpen = ref(false);
</script>

<template>
  <div>
    <button
      class="group flex w-full flex-row items-center justify-between gap-2 bg-slate-100 p-2 text-left hover:bg-slate-200 dark:bg-gray-700 dark:hover:bg-gray-600"
      @click="setCurentAddress()"
    >
      <div>
        <PowerCircle
          v-if="!active"
          class="h-4 w-4 text-gray-400 opacity-0 transition-all group-hover:opacity-100"
        />
        <PowerCircle class="h-4 w-4 text-green-500" v-if="active" />
      </div>

      <span
        class="font-mono text-xs font-semibold"
        :class="[!active && 'opacity-50']"
      >
        {{ store.accountFromPrivateKey(privateKey).address }}
      </span>

      <TrashIcon
        v-if="canDelete"
        class="h-4 w-4 text-gray-400 opacity-0 transition-all hover:text-red-500 group-hover:opacity-100"
        @click.stop="deleteModalOpen = true"
      />
    </button>

    <ConfirmationModal
      :open="deleteModalOpen"
      @close="deleteModalOpen = false"
      @confirm="deleteAddress"
      buttonText="Delete account"
      dangerous
    >
      <template #title>Delete Account</template>
      <template #description
        >Are you sure you want to delete this account?</template
      >
      <template #info>
        <div class="font-mono text-xs">
          {{ store.accountFromPrivateKey(privateKey).address }}
        </div>
      </template>
    </ConfirmationModal>
  </div>
</template>
