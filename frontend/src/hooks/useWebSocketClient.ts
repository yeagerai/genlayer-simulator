import { io } from 'socket.io-client';

export function useWebSocketClient() {
  const webSocketClient = io(import.meta.env.VITE_WS_SERVER_URL);

  webSocketClient.on('connect', () => {
    console.log('webSocketClient.connect', webSocketClient.id);
  });

  webSocketClient.on('disconnect', () => {
    console.log('webSocketClient.disconnnect', webSocketClient.id);
  });

  return webSocketClient;
}
