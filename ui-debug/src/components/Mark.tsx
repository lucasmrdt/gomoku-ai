import React from 'react';
import {StyleSheet, css} from 'aphrodite';
import {formatNumber} from '../utils/formatUtils';

import {Owner} from '../types/gomokuTypes';

const styles = StyleSheet.create({
  mark: {
    position: 'absolute',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: 14,
    fontSize: 8,
  },
  player1: {
    color: 'white',
  },
  player2: {
    color: 'black',
  },
});

interface Props {
  points: [Owner, Owner],
  className?: string,
};

const Mark = ({points: [player1, player2], className=''}: Props) => (
  <div className={`${css(styles.mark)} ${className}`}>
    <p className={css(styles.player1)}>{formatNumber(player1)}</p>
    <p className={css(styles.player2)}>{formatNumber(player2)}</p>
  </div>
);

export default React.memo<Props>(Mark);
