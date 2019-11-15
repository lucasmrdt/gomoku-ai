from .player import Player
from .cell import Cell
from abstract import ABoard
from settings import DEFAULT_BOARD_SIZE

class Board(ABoard):
  def __init__(self):
    self.size = DEFAULT_BOARD_SIZE
    self.move_listeners = []
    self.__initialize()

  def __initialize(self):
    """Initialize the board."""
    size = self.size
    self.stalked_cells = set()
    self.matrix = [[Cell(x, y) for x in range(size)] for y in range(size)]

  def set_size(self, size):
    assert 0 < size <= 20, 'size must be contains in ]0, 20]'
    self.size = size

  def reset(self):
    self.__initialize()

  def move_player(self, player, x, y):
    assert self.matrix, 'board must be initialized'
    assert isinstance(player, Player), 'player must be instance of Player'
    assert player.is_someone(), 'player must be OPPONENT or ME'
    assert 0 <= x < self.size, f'x must be contains in range [0,{self.size}['
    assert 0 <= y < self.size, f'y must be contains in range [0,{self.size}['
    assert self.is_free(x, y), f'cell at ({x},{y}) is already busy'

    self.matrix[y][x].owner = player
    for listener in self.move_listeners:
      listener(player, x, y)

  def refresh_board(self, new_positions):
    assert self.is_empty(), 'you must first clear the board before refresh it'

    for x, y, player in new_positions:
      self.move_player(player, x, y)

  def listen_move_player(self, fct):
    self.move_listeners.append(fct)

  def get_cell_at(self, x, y):
    return self.matrix[y][x] if self.is_valid_coordinate(x, y) else None

  def is_empty(self):
    return all(all(cell.owner == Player.NOBODY for cell in line) for line in self.matrix)

  def is_free(self, x, y):
    return self.matrix[y][x].owner == Player.NOBODY

  def is_valid_coordinate(self, x, y):
    return  0 <= x < self.size and 0 <= y < self.size
