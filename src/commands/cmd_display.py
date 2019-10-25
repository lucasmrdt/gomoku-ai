from protocol.io import IO
from board import Player
from .command import Command, InvalidParamsCommand

class CMD_DISPLAY(Command):
  name = 'DISPLAY'

  def __init__(self, game):
    super().__init__(game)

  def run(self):
    board = self.game.board
    assert board.matrix, 'you must first initialize the board'

    for line in board.matrix:
      self.send_message(' '.join(map(str, line)))
