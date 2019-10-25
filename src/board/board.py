from .player import Player
from abstract import ABoard

class Board(ABoard):
  matrix = None
  size = None
  avaible_positions = []

  def set_size(self, size):
    assert 0 < size <= 20, 'Size must be contains in ]0, 20]'

    self.size = size
    self.matrix = [[Player.NOBODY for _ in range(size)] for _ in range(size)]
    self.avaible_positions = [(i//size, i%size) for i in range(size*size)]

  def player_move(self, player: Player, x: int, y: int):
    assert self.matrix, 'board must be initialized before making move'
    assert isinstance(player, Player), 'player must be instance of Player'
    assert player.isSomeone(), 'player must be OPPONENT or ME'
    assert 0 <= x < self.size, f'x must be contains in range [0,{self.size}['
    assert 0 <= y < self.size, f'y must be contains in range [0,{self.size}['
    assert self.matrix[y][x] == Player.NOBODY, f'cell at ({x},{y}) is already busy'

    self.matrix[y][x] = player
    self.avaible_positions.remove((x, y))

  def clear_board(self):
    assert self.size, 'size must be specified before clear'
    self.matrix = [[Player.NOBODY for _ in range(self.size)] for _ in range(self.size)]

  def is_empty(self):
    assert self.matrix, 'you must first initialize the board size'
    return all(all(player == Player.NOBODY for player in line) for line in self.matrix)

  def refresh_board(self, new_positions):
    assert self.matrix, 'you must first initialize the board size'
    assert self.is_empty(), 'you must first clear the board before refresh it'

    for x, y, player in new_positions:
      assert 0 <= x < self.size, f'x must be contains in range [0,{self.size}['
      assert 0 <= y < self.size, f'y must be contains in range [0,{self.size}['
      assert isinstance(player, Player), 'player must be instance of Player'
      assert player.isSomeone(), 'player must be OPPONENT or ME'

      self.matrix[y][x] = player
