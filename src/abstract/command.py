from abc import ABC, abstractmethod

from .game import AGame

class ACommand(ABC):
  game: AGame
  name: str

  @abstractmethod
  def send_ok(self):
    """Send OK answer to Gomoku Narabe program."""
    raise NotImplementedError()

  @abstractmethod
  def send_position(self, x: int, y: int):
    """Send position (x,y) to Gomoku Narabe program."""
    raise NotImplementedError()

  @abstractmethod
  def send_message(self, message: str):
    """Send message to Gomoku Narabe program."""
    raise NotImplementedError()

  @abstractmethod
  def send_data(self, data: str):
    """Send data to Gomoku Narabe program."""
    raise NotImplementedError()

  @abstractmethod
  def get_params(self, nb_params):
    """Get parameters of the current command.

    nb_params -- number of expected parameters
    """
    raise NotImplementedError()

  @abstractmethod
  def get_multiline_params(self):
    """Get multiline parameters, like with the command BOARD"""
    raise NotImplementedError()

  @abstractmethod
  def run(self):
    """Execute the command"""
    raise NotImplementedError()
