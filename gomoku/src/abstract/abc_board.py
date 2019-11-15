from abc import ABC, abstractmethod

class ABoard(ABC):
  matrix: [[]] # Board matrix
  size: int # Board size
  move_listeners: [] # Move listeners
  stalked_cells: set() # All cells wich are linked to played cells

  @abstractmethod
  def set_size(self, size):
    """Set the board size.

    size -- the size integer (must be > 0)
    """
    raise NotImplementedError()

  @abstractmethod
  def reset(self):
    """Reset properties of board."""
    raise NotImplementedError()

  @abstractmethod
  def move_player(self, player, x, y):
    """Move the player (ME or OPPONENT) to (x, y) on the board.

    player -- the player (ME or OPPONENT)
    x      -- x coordinate of the move
    y      -- y coordinate of the move
    """
    raise NotImplementedError()

  @abstractmethod
  def refresh_board(self, new_positions):
    """Refresh entire board from new_positions.

    new_positions -- List of (x, y, player) with player is OPPONENT or ME
    """
    raise NotImplementedError()

  @abstractmethod
  def reset(self):
    """Clear the entire board."""
    raise NotImplementedError()

  @abstractmethod
  def listen_move_player(self, fct):
    """Listen all player move.

    fct -- Listener called with arguments (player, x, y)
    """

  @abstractmethod
  def get_cell_at(self, x, y):
    """Get cell at x y.

    x -- x position
    y -- y position
    return -- Cell or None if not found.
    """
    raise NotImplementedError()

  @abstractmethod
  def is_empty(self) -> bool:
    """Test if board is empty."""
    raise NotImplementedError()

  @abstractmethod
  def is_free(self, x, y) -> bool:
    """Test if cell at (x, y) in board is free."""
    raise NotImplementedError()

  @abstractmethod
  def is_valid_coordinate(self, x, y):
    """Test if (x, y) is a valid coordinate."""
    raise NotImplementedError()
