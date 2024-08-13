import { usePlausible } from 'v-plausible/vue';
import { type EventName, type EventProperties } from '@/types';

export const useEventTracking = () => {
  // This enables/disables the tracking of events
  // It could be defined based on the environment or a user setting like
  // `import.meta.env.MODE === 'development';`
  const isTrackingEnabled = true;
  const { trackEvent: trackPlausibleEvent } = usePlausible();

  const trackEvent = <T extends EventName>(
    name: T,
    properties?: EventProperties[T],
  ) => {
    try {
      console.debug(
        `Track Event${isTrackingEnabled ? '' : ' (blocked in dev mode)'}`,
        {
          name,
          properties,
        },
      );
      if (isTrackingEnabled) {
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
