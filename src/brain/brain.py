import random

from board import Player
from abstract import ABrain, ABoard

class Brain(ABrain):
  suggested_moves = set()

  def __init__(self, board: ABoard):
    board.listen_player_move(self.on_player_make_move)
    self.board = board

  def make_move(self, x: int, y: int):
    self.board.player_move(Player.ME, x, y)

  def on_player_make_move(self, player, x, y):
    neighbours = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    size = self.board.size

    if (x, y) in self.suggested_moves:
      self.suggested_moves.remove((x, y))

    for neighbour_x, neighbour_y in neighbours:
      pos_x, pos_y = x + neighbour_x, y + neighbour_y
      if 0 <= pos_x < size  \
      and 0 <= pos_y < size \
      and self.board.is_free(pos_x, pos_y):
        self.suggested_moves.add((pos_x, pos_y))

  def turn(self):
    # Not implemented yet, just make random move
    board = self.board

    if len(self.suggested_moves):
      selected_position = random.randint(0, len(self.suggested_moves)-1)
      x, y = list(self.suggested_moves)[selected_position]
    else:
      selected_position = random.randint(0, len(board.avaible_positions)-1)
      x, y = board.avaible_positions[selected_position]

    self.make_move(x, y)
    return x, y
