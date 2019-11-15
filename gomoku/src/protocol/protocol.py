from commands import UnknownCommand, InvalidParamsCommand, AVAIBLE_COMMANDS
from abstract import AProtocol, AGame
from .io import IO

class Protocol(AProtocol):
  def __init__(self, game: AGame):
    assert isinstance(game, AGame), 'game must be a Gomoku'

    self.game = game
    self.avaible_commands = dict((command.name, command(game)) for command in AVAIBLE_COMMANDS)

  def launch_next_command(self):
    try:
      command_name = IO.get_next_command()
      if not command_name:
        return

      command = self.avaible_commands.get(command_name, None)
      if not command:
        raise UnknownCommand(command_name)

      command.run()
    except UnknownCommand:
      IO.write_error(f'UNKNOWN {command_name} is not recognized')
    except (InvalidParamsCommand, AssertionError) as e:
      IO.write_error(f'ERROR {str(e)}')
