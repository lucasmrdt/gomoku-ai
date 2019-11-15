import operator

from board import Player, Cell
from abstract import ABrain, ABoard

class Brain(ABrain):
  def __init__(self, board: ABoard):
    board.listen_move_player(self.__on_move_player)
    self.board = board

  def __get_rewards_from_angle(self, position, direction_index, angle):
    """Get reward from angle. An angle is an oriented direction.
    Eg. Up is the angle of vertical direction.

    position -- (x, y) position of player
    direction_index -- the index of direction in Cell.DIRECTIONS
    angle -- (x, y) tupple determine the orientation of direction
    return -- new_rewards, rewards (new_rewards is used to override
              previous cell point whereas the reward incrementator)
    """
    x, y = position

    # Take the actual cell at position
    cell = self.board.matrix[y][x]
    cell_owner = cell.owner
    cell_value = cell.points_by_directions[direction_index][cell_owner.index()]

    # Take the neighbour at angle
    current = map(operator.add, position, angle)
    current = self.board.get_cell_at(*current)
    if not current:
      return 0, 0
    current_owner = cell.owner if current.is_free() else current.owner
    current_value = current.points_by_directions[direction_index][current_owner.index()]

    # Take the neighbour at opposite angle
    opposite = map(operator.sub, position, angle)
    opposite = self.board.get_cell_at(*opposite)
    opposite_owner = opposite.owner if opposite and opposite.is_busy() else cell.owner

    # If we put a cell next to an enemy malus of -0.5 is spreaded :
    # Take the owner is "O", we add new cell so we spread 1 + -0.5(malus) = 0.5
    # -.5 <- [X][P][O] -> .5 (1 - .5)
    if current_owner != cell_owner or current_owner != opposite_owner:
      return 0, (.5 if current_owner == cell_owner else -.5)

    # If the opposite cell is free we spread 1 :
    # 1 <- [X][X][P][.]
    #         cur   opp
    if opposite and opposite.is_free():
      return 0, 1

    # If the current cell is free we spread cell_value + 1 :
    # [X][X][P][.] -> 3
    #    opp   curr
    if current.is_free():
      return 0, cell_value + 1

    # Else we replace the target value by cell_value + 1 :
    # [X][X][P][X][X] -> 5
    return cell_value + 1, 0

  def __update_points_from_angle(self, current_player, position, direction_index, angle):
    """Update points from an oriented direction and an position. This function
    will compute an reward for the angle and than spread it out following the oriented direction.
    When we reach an extremium we apply the reward to the extremium cell.

    current_player -- cell owner
    position -- (x, y) position of player
    direction_index -- the index of direction in Cell.DIRECTIONS
    angle -- (x, y) tupple determine the orientation of direction
    """
    player = None
    points = None
    cell = None
    board_size = self.board.size
    matrix = self.board.matrix

    new_rewards, rewards = self.__get_rewards_from_angle(position, direction_index, angle)

    while True:
      position = tuple(map(operator.add, position, angle))
      x, y = position

      # If position is outside the board : STOP
      if not self.board.is_valid_coordinate(x, y):
        break

      cell = matrix[y][x]
      points = cell.points_by_directions[direction_index]

      # Player is the current player which has played (the first cell)
      if not player:
        player = cell.owner if cell.is_busy() else current_player

      # If we found an different player that the current : STOP
      if cell.owner != player:
        break

    if not cell or not points or not cell.is_free():
      return None

    if rewards:
      points[player.index()] += rewards
    elif new_rewards:
      points[player.index()] = new_rewards
    cell.compute_weight()
    return cell

  def __on_move_player(self, player, x, y):
    """When a player made move we refresh the weight related to the played player's position."""
    matrix = self.board.matrix
    position = x, y
    cell = matrix[y][x]
    points_by_directions = cell.points_by_directions

    # The played cell is no longer stalked
    if cell in self.board.stalked_cells:
      self.board.stalked_cells.remove(cell)

    # Update points for each angles of each directions from the played point (x, y)
    for direction_index, direction in enumerate(Cell.DIRECTIONS):
      for angle in direction:
        updated_cell = self.__update_points_from_angle(player, position, direction_index, angle)
        if updated_cell and not updated_cell in self.board.stalked_cells:
          self.board.stalked_cells.add(updated_cell)

      # Increment each directions points of player cell
      points_by_directions[direction_index][player.index()] += 1

  def __get_next_move(self):
    """Get the next move. Critical moves are prioritized."""
    criticals = []
    for cell in self.board.stalked_cells:
      if cell.is_critical():
        criticals.append(cell)
    if criticals:
      return max(criticals, key=lambda x: x.max_points)
    return max(self.board.stalked_cells) if self.board.stalked_cells else None

  def turn(self):
    board_size = self.board.size
    cell = self.__get_next_move()

    # If weight is null, we're the first to play
    if not cell:
      x, y = board_size//2, board_size//2
    else:
      x, y = cell.x, cell.y

    self.board.move_player(Player.ME, x, y)
    return x, y
