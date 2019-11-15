from .command import Command, InvalidParamsCommand

class CMD_INFO(Command):
  name = 'INFO'

  def __init__(self, game):
    super().__init__(game)

  def run(self):
    _ = self.get_params()
    # Don't use informations 🤫
