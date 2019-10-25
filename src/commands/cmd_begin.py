from .command import Command, InvalidParamsCommand
from protocol.io import IO

class CMD_BEGIN(Command):
  name = 'BEGIN'

  def __init__(self, game):
    super().__init__(game)

  def run(self):
    board = self.game.board

    assert board.is_empty(), 'the board must be empty'

    x, y = self.game.brain.turn()
    self.send_position(x, y)
