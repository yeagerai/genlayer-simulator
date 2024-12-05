export const useConfig = () => {
  const studioVersion = import.meta.env.VITE_APP_VERSION || 'unknown';
  const isHostedEnvironment = import.meta.env.VITE_IS_HOSTED === 'true';
  const canUpdateValidators = !isHostedEnvironment;
  const canUpdateProviders = !isHostedEnvironment;

  return {
    studioVersion,
    canUpdateValidators,
    canUpdateProviders,
  };
};
