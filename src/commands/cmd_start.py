from .command import Command, InvalidParamsCommand

class CMD_START(Command):
  name = 'START'

  def __init__(self, game):
    super().__init__(game)

  def run(self):
    size, = self.get_params(1)

    try:
      size = int(size)
    except ValueError:
      raise InvalidParamsCommand(f'size must be an integer')

    self.game.is_running = True
    self.game.board.set_size(size)
    self.game.board.reset()
    self.send_ok()
