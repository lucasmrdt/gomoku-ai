from .command import Command, InvalidParamsCommand
from settings import INFORMATIONS

class CMD_ABOUT(Command):
  name = 'ABOUT'

  def __init__(self, game):
    super().__init__(game)

  def run(self):
    message = ', '.join(f'{key}="{value}"' for key, value in INFORMATIONS.items())
    self.send_data(message)
