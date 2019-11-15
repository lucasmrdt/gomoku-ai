import React from 'react';
import {StyleSheet, css} from 'aphrodite';
import {formatNumber} from '../utils/formatUtils';
import Mark from './Mark';

import {Cell} from '../types/gomokuTypes';

const BACKGROUND_COLOR = '#E4AF5A';
const EVALUATION_MARKER_SIZE = 48;

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    background: BACKGROUND_COLOR,
    pointerEvents: 'none',
    zIndex: 100,
    opacity: 0.75,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  horizontalLeft: {
    top: '50%',
    left: 0,
    transform: 'translateY(-50%)',
  },
  horizontalRight: {
    top: '50%',
    right: 0,
    transform: 'translateY(-50%)',
  },
  verticalTop: {
    top: 0,
    left: '50%',
    transform: 'translateX(-50%)',
  },
  verticalBottom: {
    bottom: 0,
    left: '50%',
    transform: 'translateX(-50%)',
  },
  topLeftCorner: {
    top: 0,
    left: 0,
  },
  bottomRightCorner: {
    right: 0,
    bottom: 0,
  },
  topRightCorner: {
    top: 0,
    right: 0,
  },
  bottomLeftCorner: {
    bottom: 0,
    left: 0,
  }
});

interface Props {
  cell: Cell,
  position: {
    left: number,
    top: number,
  },
};

const Evaluation = ({cell, position}: Props) => (cell.isFree
  ? (
    <div
      className={css(styles.container)}
      style={{
        width: EVALUATION_MARKER_SIZE,
        height: EVALUATION_MARKER_SIZE,
        left: position.left - EVALUATION_MARKER_SIZE/2,
        top: position.top - EVALUATION_MARKER_SIZE/2
      }}
    >
      <Mark
        className={css(styles.horizontalLeft)}
        points={cell.neighbours.horizontal}
      />
      <Mark
        className={css(styles.horizontalRight)}
        points={cell.neighbours.horizontal}
      />

      <Mark
        className={css(styles.verticalTop)}
        points={cell.neighbours.vertical}
      />
      <Mark
        className={css(styles.verticalBottom)}
        points={cell.neighbours.vertical}
      />

      <Mark
        className={css(styles.topLeftCorner)}
        points={cell.neighbours.leftCorner}
      />
      <Mark
        className={css(styles.bottomRightCorner)}
        points={cell.neighbours.leftCorner}
      />

      <Mark
        className={css(styles.topRightCorner)}
        points={cell.neighbours.rightCorner}
      />
      <Mark
        className={css(styles.bottomLeftCorner)}
        points={cell.neighbours.rightCorner}
      />

      <p>{formatNumber(cell.weight)}</p>
    </div>
  )
  : null
);

export default React.memo<Props>(Evaluation);
