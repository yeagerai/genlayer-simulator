import { useGtm } from '@gtm-support/vue-gtm';

export const useEventTracking = () => {
  const isLocalDebugMode = import.meta.env.MODE === 'development';
  const gtm = useGtm();

  const trackEvent = (name: string, label: string, value: any) => {
    try {
      const eventData = {
        event: name,
        category: 'button',
        action: 'click',
        label,
        value,
      };

      if (isLocalDebugMode) {
        console.debug('Mock Track Event', eventData);
      } else if (gtm?.enabled()) {
        gtm.trackEvent(eventData);
      } else {
        console.error('GTM not initialized');
      }
    } catch (err) {
      console.error('Failed to track event', err);
    }
  };

  return {
    trackEvent,
  };
};
