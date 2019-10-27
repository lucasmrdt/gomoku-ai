from board import Player
from .command import Command, InvalidParamsCommand

class CMD_BOARD(Command):
  name = 'BOARD'

  def __init__(self, game):
    super().__init__(game)

  def run(self):
    board = self.game.board
    positions = self.get_multiline_params()
    new_board_positions = []

    for position in positions:
      try:
        x, y, field = map(int, position)
      except ValueError:
        raise InvalidParamsCommand(f'parameters must be integers with this format "x,y,field"')

      try:
        player = Player(field)
        assert player.isSomeone()
      except (ValueError, AssertionError):
        raise InvalidParamsCommand(f'invalid type of player, {field} is not recognized')

      new_board_positions.append((x, y, player))

    board.refresh_board(new_board_positions)
    x, y = self.game.brain.turn()
    self.send_position(x, y)
