import { useGtm } from '@gtm-support/vue-gtm';

const isLocalMode = import.meta.env.MODE === 'development';
const gtm = useGtm();

export const useEventTracking = () => {
  const trackEvent = (name: string, label: string, value: any) => {
    try {
      const eventData = {
        event: name,
        category: 'button',
        action: 'click',
        label,
        value,
      };

      if (isLocalMode) {
        console.debug('trackEvent', eventData);
      } else {
        gtm?.trackEvent(eventData);
      }
    } catch (err) {
      console.error('Failed to track event', err);
    }
  };

  return {
    trackEvent,
  };
};
