import { usePlausible } from 'v-plausible/vue';
import { type EventName, type EventProperties } from '@/types';

export const useEventTracking = () => {
  const isDevelopment = false; // TODO:
  // const isDevelopment = import.meta.env.MODE === 'development';
  const { trackEvent: trackPlausibleEvent } = usePlausible();

  const trackEvent = <T extends EventName>(
    name: T,
    properties?: EventProperties[T]
  ) => {
    try {
      if (isDevelopment) {
        console.debug('Track Event (mock)', { name, properties });
      } else {
        console.debug('Track Event', { name, properties });
        trackPlausibleEvent(name, { props: properties });
      }
    } catch (err) {
      console.error('Failed to track event', err);
    }
  };

  return {
    trackEvent,
  };
};
