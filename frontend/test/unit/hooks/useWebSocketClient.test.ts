import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useWebSocketClient } from '@/hooks/useWebSocketClient';
import { io, type Socket } from 'socket.io-client';

const mockSocket: Partial<Socket> = {
  id: 'mocked-socket-id',
  on: vi.fn(),
};

vi.mock('socket.io-client', () => ({
  io: vi.fn(() => mockSocket),
}));

describe('useWebSocketClient', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should create a WebSocket client with the correct URL', () => {
    useWebSocketClient();
    expect(io).toHaveBeenCalledWith(import.meta.env.VITE_WS_SERVER_URL);
  });

  it('should set up connect and disconnect event handlers', () => {
    const consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

    useWebSocketClient();

    expect(mockSocket.on).toHaveBeenCalledWith('connect', expect.any(Function));
    expect(mockSocket.on).toHaveBeenCalledWith(
      'disconnect',
      expect.any(Function),
    );

    const connectCallback = (mockSocket.on as any).mock.calls.find(
      (call: any) => call[0] === 'connect',
    )[1];
    connectCallback();
    expect(consoleLogSpy).toHaveBeenCalledWith(
      'webSocketClient.connect',
      mockSocket.id,
    );

    const disconnectCallback = (mockSocket.on as any).mock.calls.find(
      (call: any) => call[0] === 'disconnect',
    )[1];
    disconnectCallback();
    expect(consoleLogSpy).toHaveBeenCalledWith(
      'webSocketClient.disconnnect',
      mockSocket.id,
    );

    consoleLogSpy.mockRestore();
  });
});
