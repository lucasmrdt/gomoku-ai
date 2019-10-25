import re

from protocol.constants import DONE, PARAMS_SPLITTER, RETURN_LINE
from protocol.io import IO
from abstract import ACommand, AGame

class UnknownCommand(Exception):
  """Raised when the command is unknown"""
  pass

class InvalidParamsCommand(Exception):
  """Raised when the command is provided with invalid params"""
  pass

class Command(ACommand):
  def __init__(self, game: AGame):
    assert isinstance(game, AGame), 'game must be a Gomoku'

    self.game = game

  def __str__(self):
    return self.name

  def send_ok(self):
    IO.write_standard('OK')

  def send_position(self, x: int, y: int):
    IO.write_standard(f'{x},{y}')

  def send_data(self, data: str):
    IO.write_standard(data)

  def send_message(self, message: str):
    IO.write_standard(f'MESSAGE {message}')

  def get_params(self, nb_params: int=None):
    params = IO.get_params()
    splitted_params = re.split(PARAMS_SPLITTER, params)
    if nb_params:
      assert len(splitted_params) == nb_params, f'expected {nb_params} parameters but got {len(splitted_params)}'
    return splitted_params

  def get_multiline_params(self):
    params = IO.get_params(end=DONE)
    return [re.split(PARAMS_SPLITTER, line) for line in params.split(RETURN_LINE)]
