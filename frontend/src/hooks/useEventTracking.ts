import { useGtm } from '@gtm-support/vue-gtm';

export const useEventTracking = () => {
  const isDevelopment = import.meta.env.MODE === 'development';

  const trackEvent = (name: string, label: string, value: any) => {
    const gtm = useGtm();
    
    try {
      const eventData = {
        event: name,
        category: 'button',
        action: 'click',
        label,
        value,
      };

      if (isDevelopment) {
        console.debug('Track Event (mock)', eventData);
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
