from abc import ABC, abstractmethod

from .abc_board import ABoard
from .abc_protocol import AProtocol
from .abc_brain import ABrain

class AGame(ABC):
  board: ABoard
  protocol: AProtocol
  brain: ABrain
  informations: dict
  is_running: bool

  @abstractmethod
  def start(self):
    raise NotImplementedError()

  @abstractmethod
  def stop(self):
    raise NotImplementedError()
