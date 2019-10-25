from .command import Command, InvalidParamsCommand

class CMD_RESTART(Command):
  name = 'RESTART'

  def __init__(self, game):
    super().__init__(game)

  def run(self):
    self.game.is_running = True
    self.game.board.clear_board()
    self.send_ok()
