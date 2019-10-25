import random

from board import Player
from abstract import ABrain, ABoard

class Brain(ABrain):
  def __init__(self, board: ABoard):
    self.board = board

  def make_move(self, x: int, y: int):
    self.board.player_move(Player.ME, x, y)

  def turn(self):
    # Not implemented yet, just make random move
    board = self.board
    selected_position = random.randint(0, len(board.avaible_positions)-1)
    x, y = board.avaible_positions[selected_position]

    self.make_move(x, y)
    return x, y
