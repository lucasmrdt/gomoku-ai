from .command import Command, InvalidParamsCommand

class CMD_END(Command):
  name = 'END'

  def __init__(self, game):
    super().__init__(game)

  def run(self):
    self.game.is_running = False
