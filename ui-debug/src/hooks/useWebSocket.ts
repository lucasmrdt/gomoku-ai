import {useEffect, useCallback, useRef} from 'react';

interface Props {
  onMessage: (data: any) => void,
  ip: string,
  port: number,
};

const useWebSocket = ({onMessage, ip, port}: Props) => {
  const wsRef = useRef<WebSocket | null>(null);

  const sendData = useCallback(data => {
    const ws = wsRef.current;
    if (!ws || ws.readyState !== ws.OPEN) {
      return;
    }
    ws.send(JSON.stringify(data));
  }, []);

  useEffect(() => {
    const connect = () => {
      const ws = new WebSocket(`ws://${ip}:${port}/`);

      ws.onclose = () => {
        console.warn('Reconnection to AI...');
        setTimeout(connect, 1000);
      };

      ws.onopen = () => {
        console.log('AI is now connected.');
        wsRef.current = ws;
      };

      ws.onmessage = ({data}) => {
        onMessage(JSON.parse(data));
      };
    };

    connect();
  }, [onMessage, ip, port]);

  return sendData;
};

export default useWebSocket;
