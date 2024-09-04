import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useEventTracking } from '@/hooks';

const testEvent = 'called_read_method';
const testProperties = { contract_name: 'test', method_name: 'test' };

const trackPlausibleEventMock = vi.fn();

vi.mock('v-plausible/vue', () => ({
  usePlausible: vi.fn(() => ({
    trackEvent: trackPlausibleEventMock,
  })),
}));

describe('useEventTracking composable', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should log event tracking in development mode without calling trackPlausibleEvent', () => {
    import.meta.env.MODE = 'development';
    const consoleDebugSpy = vi
      .spyOn(console, 'debug')
      .mockImplementation(() => {}); // Mock to avoid console output

    const { trackEvent } = useEventTracking();
    trackEvent(testEvent, testProperties);

    expect(consoleDebugSpy).toHaveBeenCalledWith(
      'Track Event (blocked in dev mode)',
      { name: testEvent, properties: testProperties },
    );
    expect(trackPlausibleEventMock).not.toHaveBeenCalled();
    consoleDebugSpy.mockRestore();
  });

  it('should call trackPlausibleEvent in production mode', () => {
    import.meta.env.MODE = 'production';
    const consoleDebugSpy = vi
      .spyOn(console, 'debug')
      .mockImplementation(() => {}); // Mock to avoid console output

    const { trackEvent } = useEventTracking();
    trackEvent(testEvent, testProperties);

    expect(consoleDebugSpy).toHaveBeenCalledWith('Track Event', {
      name: testEvent,
      properties: testProperties,
    });
    expect(trackPlausibleEventMock).toHaveBeenCalledWith(testEvent, {
      props: testProperties,
    });
    consoleDebugSpy.mockRestore();
  });

  it('should log an error if tracking fails', () => {
    import.meta.env.MODE = 'production';
    const consoleErrorSpy = vi
      .spyOn(console, 'error')
      .mockImplementation(() => {}); // Mock to avoid console output
    const consoleDebugSpy = vi
      .spyOn(console, 'debug')
      .mockImplementation(() => {}); // Mock to avoid console output

    trackPlausibleEventMock.mockImplementationOnce(() => {
      throw new Error('Mock error');
    });

    const { trackEvent } = useEventTracking();
    trackEvent(testEvent, testProperties);

    expect(consoleErrorSpy).toHaveBeenCalledWith(
      'Failed to track event',
      expect.any(Error),
    );
    expect(consoleDebugSpy).toHaveBeenCalledWith('Track Event', {
      name: testEvent,
      properties: testProperties,
    });

    consoleErrorSpy.mockRestore();
    consoleDebugSpy.mockRestore();
  });
});
