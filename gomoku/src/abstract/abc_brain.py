from abc import ABC, abstractmethod

from .abc_board import ABoard

class ABrain(ABC):
  board: ABoard

  @abstractmethod
  def turn(self) -> (int, int):
    """Must choose a good position, play it and return it.

    return -- x, y (chosen position)
    """
    raise NotImplementedError()
