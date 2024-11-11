import { ref, computed } from 'vue';

export const useConfig = () => {
  const isLocalNetwork = ref(window.location.href.includes('localhost'));

  const canUpdateValidators = computed(() => isLocalNetwork.value);

  return {
    canUpdateValidators,
  };
};
