import {GOMOKU_PLAYER} from '../contants/Gomoku';

import {Owner} from '../types/gomokuTypes';

export const remotePlayerToLocal = (remotePlayer: Owner) => (
  remotePlayer
  && (remotePlayer === GOMOKU_PLAYER.me.ws
  ? GOMOKU_PLAYER.me.local
  : GOMOKU_PLAYER.opponent.local)
);

export const localPlayerToRemote = (localPlayer: Owner) => (
  localPlayer
  && (localPlayer === GOMOKU_PLAYER.me.local
  ? GOMOKU_PLAYER.me.ws
  : GOMOKU_PLAYER.opponent.ws)
);
