from .command import Command, InvalidParamsCommand
from board import Player
from protocol.io import IO

class CMD_TURN(Command):
  name = 'TURN'

  def __init__(self, game):
    super().__init__(game)

  def run(self):
    board = self.game.board
    x, y = self.get_params(2)

    try:
      opponent_x, opponent_y = int(x), int(y)
    except ValueError:
      raise InvalidParamsCommand(f'coordinates must be integers')

    board.player_move(Player.OPPONENT, opponent_x, opponent_y)
    x, y = self.game.brain.turn()
    self.send_position(x, y)
