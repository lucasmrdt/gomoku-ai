import React, {useState, useCallback} from 'react';
// @ts-ignore
import {Goban} from '@sabaki/shudan';
import {Spin, Switch} from 'antd';
import {StyleSheet, css} from 'aphrodite';
import {IP, PORT} from '../contants/Network';
import {GOMOKU_PLAYER} from '../contants/Gomoku';
import {remotePlayerToLocal} from '../utils/gomokuUtils';
import EvaluationMarker from './Evaluation';
import Position from './Position';
import useWebSocket from '../hooks/useWebSocket';

import {Cell, Owner} from '../types/gomokuTypes';

const styles = StyleSheet.create({
  switch: {
    position: 'fixed',
    top: 50,
    left: '50%',
    transform: 'translateX(-50%)',
  },
});

const App = () => {
  const [position, setPosition] = useState({top: 0, left: 0, x: 0, y: 0});

  const [localBoard, setLocalBoard] = useState<Owner[][] | null>(null);
  const [remoteBoard, setRemoteBoard] = useState<Cell[][] | null>(null);

  const [player, setPlayer] = useState(GOMOKU_PLAYER.me);
  const [withAI, setAI] = useState(true);

  // Web Socket
  const onReceiveRemoteData = useCallback((remoteBoard: Cell[][]) => {
    const localBoard = remoteBoard.map(row => row.map(({owner}) => remotePlayerToLocal(owner)));
    setRemoteBoard(remoteBoard);
    setLocalBoard(localBoard);
  }, [setLocalBoard, setRemoteBoard]);

  const sendMessage = useWebSocket({onMessage: onReceiveRemoteData, ip: IP, port: PORT});

  const sendMove = useCallback(({x, y, movingPlayer}) => (
    sendMessage({x, y, player: movingPlayer.ws, ai: withAI})
  ), [withAI, sendMessage]);

  // Event Handlers
  const toggleAI = useCallback(checked => setAI(checked), [setAI]);

  const onVertexMouseEnter = useCallback(({currentTarget}, [x, y]) => {
    const {left, top, height, width} = currentTarget.getBoundingClientRect();
    setPosition({left: left + width/2, top: top + height/2, x, y});
  }, [setPosition]);

  const onVertexClick = useCallback((__, [x, y]) => {
    if (!remoteBoard || !remoteBoard[y][x].isFree) {
      return console.warn(`Cell at ${x}, ${y} is already busy.`);
    }

    sendMove({x, y, movingPlayer: player});
    if (!withAI) {
      setPlayer(player === GOMOKU_PLAYER.me ? GOMOKU_PLAYER.opponent : GOMOKU_PLAYER.me);
    }
  }, [remoteBoard, sendMove, setPlayer, player, withAI]);

  return (
    <div className={'app'}>
      {!localBoard || !remoteBoard
        ? <Spin />
        : [
          <Position position={position} />,
          <Switch
            className={css(styles.switch)}
            checked={withAI}
            onChange={toggleAI} />,
          <Goban
            showCoordinates
            signMap={localBoard}
            onVertexMouseEnter={onVertexMouseEnter}
            onVertexClick={onVertexClick}
          />,
          !withAI && (
            <EvaluationMarker
              position={position}
              cell={remoteBoard[position.y][position.x]} />
          )
        ]
      }
    </div>
  );
}

export default App;
