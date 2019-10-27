from .player import Player
from abstract import ABoard
from settings import DEFAULT_BOARD_SIZE

import os

class Cell:
  BALANCE = 0.8
  DIRECTIONS = [
    # format (y, x)
    ((1, 0), (-1, 0)),  # Vertical line
    ((0, 1), (0, -1)),  # Horizontal line
    ((-1, 1), (1, -1)), # Diagonal line (up-right to bottom-left)
    ((-1, -1), (1, 1)), # Diagonal line (up-left to bottom-right)
  ]

  def __init__(self):
    self.points_by_directions = [[0, 0] for _ in self.DIRECTIONS]
    self.owner = Player.NOBODY
    self.weight = 0

  def __str__(self):
    return '%.1f' % self.weight if self.owner == Player.NOBODY else f' {str(self.owner)} '
    # return '[' + ','.join(':'.join(map(str, points)) for points in self.points_by_directions) + ']'

  def is_free(self):
    return self.owner == Player.NOBODY

  def is_active_direction(self, direction):
    return direction != (0, 0)

  def compute_weight(self):
    players_orders = [(0, 1), (1, 0)]
    weights = []

    for player_a, player_b in players_orders:
      active_directions = list(filter(lambda x: x[player_a], self.points_by_directions))
      total_points = sum(abs(direction[player_a] - min(1, direction[player_b])) for direction in active_directions)
      weight = total_points * self.BALANCE**max(0, len(active_directions)-1)
      weights.append(weight)
    a, b = sorted(weights, reverse=True)
    self.weight = a + b*.15

class Board(ABoard):
  matrix = None
  size = None
  avaible_positions = []
  move_listeners = []

  move_idx = 0

  def __init__(self):
    self.size = DEFAULT_BOARD_SIZE
    self.initialize()

  def set_size(self, size):
    assert 0 < size <= 20, 'size must be contains in ]0, 20]'
    self.size = size

  def initialize(self):
    size = self.size
    self.matrix = [[Cell() for _ in range(size)] for _ in range(size)]
    self.avaible_positions = [(i//size, i%size) for i in range(size*size)]

  def reset(self):
    self.initialize()

  def player_move(self, player, x, y):
    assert self.matrix, 'board must be initialized'
    assert isinstance(player, Player), 'player must be instance of Player'
    assert player.isSomeone(), 'player must be OPPONENT or ME'
    assert 0 <= x < self.size, f'x must be contains in range [0,{self.size}['
    assert 0 <= y < self.size, f'y must be contains in range [0,{self.size}['
    assert self.is_free(x, y), f'cell at ({x},{y}) is already busy'

    self.matrix[y][x].owner = player
    self.avaible_positions.remove((x, y))
    for listener in self.move_listeners:
      listener(player, x, y)
    # print('\n'.join(' '.join(map(str, line)) for line in self.matrix))
    # print()

    # with open(os.path.join(os.environ['HOMEPATH'], 'debug.txt'), 'a') as f:
    #   debug = '\n'.join(' '.join(map(str, line)) for line in self.matrix)
    #   f.write(f'MOVE {self.move_idx}:\n{debug}\n\n')
    #   f.flush()
    #   self.move_idx += 1

  def refresh_board(self, new_positions):
    assert self.is_empty(), 'you must first clear the board before refresh it'

    for x, y, player in new_positions:
      self.player_move(player, x, y)

  def listen_player_move(self, fct):
    self.move_listeners.append(fct)

  def is_empty(self):
    return all(all(cell.owner == Player.NOBODY for cell in line) for line in self.matrix)

  def is_free(self, x, y):
    return self.matrix[y][x].owner == Player.NOBODY

  def is_valid_coordinate(self, x, y):
    return  0 <= x < self.size and 0 <= y < self.size
