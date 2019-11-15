from enum import Enum

from .player import Player

class Direction(Enum):
  HORIZONTAL    = 0
  VERTICAL      = 1
  LEFT_CORNER   = 2
  RIGHT_CORNER  = 3

class Cell:
  CRITAL_THRESHOLD = 3  # Marks
  BALANCE = 0.85
  DIRECTIONS = [
    ((-1, 0), (1, 0)),  # Left to Right
    ((0, -1), (0, 1)),  # Top to bottom
    ((-1, -1), (1, 1)), # up-left to bottom-right
    ((-1, 1), (1, -1)), # bottom-left to top-right
  ]

  def __init__(self, x, y):
    self.points_by_directions = [[0, 0] for _ in self.DIRECTIONS]
    self.max_points = 0
    self.owner = Player.NOBODY
    self.weight = 0
    self.x = x
    self.y = y

  def __gt__(self, value):
    assert isinstance(value, Cell), 'unsuported comparison with non-cell instances'
    return self.weight > value.weight

  def __repr__(self):
    return f'({self.x},{self.y}) {self.weight}'

  def __eq__(self, value):
    if not isinstance(value, Cell):
      return False
    return self.x == value.x and self.y == value.y

  def __hash__(self):
    return hash(f'{self.x}{self.y}')

  def is_free(self):
    return self.owner == Player.NOBODY

  def is_busy(self):
    return not self.is_free()

  def is_critical(self):
    return self.max_points >= self.CRITAL_THRESHOLD

  def compute_weight(self):
    # players_orders = [(0, 1), (1, 0)]
    # weights = []

    # for a, b in players_orders:
    #   abs_diff = lambda direction: abs(direction[a] - min(1, direction[b]))

    #   active_directions = list(filter(lambda direction: direction[a] > 1 or direction[b] > 1, self.points_by_directions))
    #   total_points = sum(map(abs_diff, active_directions))
    #   weight = total_points * self.BALANCE**max(0, len(active_directions)-1)
    #   weights.append(weight)

    # a, b = sorted(weights, reverse=True)
    # self.weight = a + b*.15
    # self.weight = self.points_by_directions
    self.weight = max(map(max, self.points_by_directions))
    self.max_points = max(map(max, self.points_by_directions))

  def dump(self):
    return {
      'x': self.x,
      'y': self.y,
      'horizontal': self.points_by_directions[Direction.HORIZONTAL.value],
      'vertical': self.points_by_directions[Direction.VERTICAL.value],
      'leftCorner': self.points_by_directions[Direction.LEFT_CORNER.value],
      'rightCorner': self.points_by_directions[Direction.RIGHT_CORNER.value],
      'isFree': self.is_free(),
      'weight': self.weight,
      'owner': self.owner.value,
    }
