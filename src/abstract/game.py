from abc import ABC, abstractmethod

from .board import ABoard
from .protocol import AProtocol
from .brain import ABrain

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
