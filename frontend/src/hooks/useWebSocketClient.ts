import { io } from 'socket.io-client';

const webSocketClient = io(import.meta.env.VITE_WS_SERVER_URL);

export function useWebSocketClient() {
  webSocketClient.on('connect', () => {
    console.log('webSocketClient.connect', webSocketClient.id);
  });

  webSocketClient.on('disconnect', () => {
    console.log('webSocketClient.disconnnect', webSocketClient.id);
  });

  return webSocketClient;
}
