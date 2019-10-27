from .player import Player
from abstract import ABoard
from settings import DEFAULT_BOARD_SIZE

class Cell:
  BALANCE = 0.85
  LINES = [
    ((0, 1), (0, -1)),  # Vertical line
    ((1, 0), (-1, 0)),  # Horizontal line
    ((1, 1), (-1, -1)), # Diagonal line (up-right to bottom-left)
    ((1, -1), (1, -1)), # Diagonal line (up-left to bottom-right)
  ]

  def __init__(self):
    self.points_by_lines = [(0, 0) for _ in self.LINES]
    self.owner = Player.NOBODY
    self.weight = 0

  def is_active_direction(self, direction):
    return direction != (0, 0)

  def compute_weight(self):
    nb_active_directions = len(filter(self.is_active_direction, self.points_by_lines))
    total_points = sum(abs(a - b) for a, b in self.points_by_lines)
    self.weight = total_points * self.BALANCE**nb_active_directions

class Board(ABoard):
  matrix = None
  size = None
  avaible_positions = []
  move_listeners = []

  def __init__(self):
    self.size = DEFAULT_BOARD_SIZE
    self.initialize()

  def set_size(self, size):
    assert 0 < size <= 20, 'Size must be contains in ]0, 20]'
    self.size = size

  def initialize(self):
    size = self.size
    self.matrix = [[Cell() for _ in range(size)] for _ in range(size)]
    self.avaible_positions = [(i//size, i%size) for i in range(size*size)]

  def reset(self):
    self.initialize()

  def player_move(self, player: Player, x: int, y: int):
    assert self.matrix, 'board must be initialized'
    assert isinstance(player, Player), 'player must be instance of Player'
    assert player.isSomeone(), 'player must be OPPONENT or ME'
    assert 0 <= x < self.size, f'x must be contains in range [0,{self.size}['
    assert 0 <= y < self.size, f'y must be contains in range [0,{self.size}['
    assert self.matrix[y][x] == Player.NOBODY, f'cell at ({x},{y}) is already busy'

    self.matrix[y][x] = player
    self.avaible_positions.remove((x, y))
    for listener in self.move_listeners:
      listener(player, x, y)

  def refresh_board(self, new_positions):
    assert self.is_empty(), 'you must first clear the board before refresh it'

    for x, y, player in new_positions:
      self.player_move(player, x, y)

  def listen_player_move(self, fct):
    self.move_listeners.append(fct)

  def is_empty(self):
    return all(all(player == Player.NOBODY for player in line) for line in self.matrix)

  def is_free(self, x, y):
    return self.matrix[y][x] == Player.NOBODY
