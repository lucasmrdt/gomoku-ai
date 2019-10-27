from abc import ABC, abstractmethod

from .board import ABoard

class ABrain(ABC):
  board: ABoard

  @abstractmethod
  def reset(self):
    """Reset the brain."""
    raise NotImplementedError()

  @abstractmethod
  def make_move(self) -> (int, int):
    """Make the next turn and return the choice coordinnate."""
    raise NotImplementedError()

  @abstractmethod
  def on_player_move(self, player, x, y) -> (int, int):
    """Event handler when player made move."""
    raise NotImplementedError()
