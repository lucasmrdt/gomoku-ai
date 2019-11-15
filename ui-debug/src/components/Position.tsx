import React from 'react';
import {StyleSheet, css} from 'aphrodite';

const styles = StyleSheet.create({
  container: {
    position: 'fixed',
    top: 10,
    left: '50%',
    transform: 'translateX(-50%)',
  },
});

type Props = {
  position: {
    x: number,
    y: number,
  },
};

const Position = ({position}: Props) => (
  <p className={css(styles.container)}>
    {`${position.x}, ${position.y}`}
  </p>
);

export default React.memo<Props>(Position);
