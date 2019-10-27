from abc import ABC, abstractmethod

from .board import ABoard

class ABrain(ABC):
  board: ABoard

  @abstractmethod
  def reset(self):
    """Reset the brain"""
    raise NotImplementedError()

  @abstractmethod
  def turn(self) -> (int, int):
    """Make the next turn and return the choice coordinnate"""
    raise NotImplementedError()
