from abc import ABC, abstractmethod

class ABoard(ABC):
  matrix: [[]] # Board matrix
  size: int # Board size
  avaible_positions: [int] # All avaible positions
  move_listeners: [] # Move listeners

  @abstractmethod
  def set_size(self, size):
    """Set the board size.

    size -- the size integer (must be > 0)
    """
    raise NotImplementedError()

  @abstractmethod
  def initialize(self):
    """Initialize the matrix board and availables_moves."""
    raise NotImplementedError()


  @abstractmethod
  def player_move(self, player, x, y):
    """Move the player (ME or OPPONENT) to (x, y) on the board.

    player -- the player (ME or OPPONENT)
    x      -- x coordinate of the move
    y      -- y coordinate of the move
    """
    raise NotImplementedError()

  @abstractmethod
  def reset(self):
    """Clear the entire board."""
    raise NotImplementedError()

  @abstractmethod
  def refresh_board(self, new_positions):
    """Refresh entire board from new_positions.

    new_positions -- List of (x, y, player) with player is OPPONENT or ME
    """
    raise NotImplementedError()


  @abstractmethod
  def listen_player_move(self, fct):
    """Listen all player move.

    fct -- Listener called with arguments (player, x, y)
    """

  @abstractmethod
  def is_empty(self) -> bool:
    """Test if board is empty."""
    raise NotImplementedError()

  @abstractmethod
  def is_free(self, x, y) -> bool:
    """Test if cell at (x, y) in board is free."""
    raise NotImplementedError()
