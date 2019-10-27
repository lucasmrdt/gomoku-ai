import operator
import random

from board import Player, Cell
from abstract import ABrain, ABoard

class Brain(ABrain):
  def __init__(self, board: ABoard):
    board.listen_player_move(self.on_player_move)
    self.board = board
    self.suggested_moves = set()

  def reset(self):
    self.suggested_moves = set()

  def make_move(self, x: int, y: int):
    self.board.player_move(Player.ME, x, y)

  def compute_new_way_weight(self, default_player, position, direction_index, way):
    # Take the current cell
    x, y = position
    cell = self.board.matrix[y][x]

    # Take the neighbour cell from the direction
    neighbour_x, neighbour_y = map(operator.add, position, way)
    if not self.board.is_valid_coordinate(neighbour_x, neighbour_y):
      return 0
    neighbour_cell = self.board.matrix[neighbour_y][neighbour_x]

    # Get the neighbour owner
    neighbour_owner = neighbour_cell.owner if neighbour_cell.owner != Player.NOBODY else default_player

    # Get the neighbour_owner value and her opponent value to.
    neighbour_value = cell.points_by_directions[direction_index][neighbour_owner.index()]
    opponent_value = cell.points_by_directions[direction_index][neighbour_owner.opponent_index()]

    # Compute the new line weight
    malus = min(1, opponent_value) # Malus can only be 0 or 1.
    return neighbour_value - malus

  def update_new_way_weight(self, default_player, position, direction_index, way):
    player = None
    board_size = self.board.size
    matrix = self.board.matrix
    new_way_weight = self.compute_new_way_weight(default_player, position, direction_index, way)

    while True:
      x, y = position
      cell = matrix[y][x]

      # If position is outside the board we stop propagate new way value.
      if not self.board.is_valid_coordinate(x, y):
        break

      # We need to track in which player we propagate the new way value.
      if not player:
        player = cell.owner if cell.owner != Player.NOBODY else default_player

      # If we found an different player that the first met, we stop propagate the new way value.
      if cell.owner != player:
        break

      cell.points_by_directions[direction_index][player.index()] = new_way_weight
      position = map(operator.add, position, way)

  def on_player_move(self, player, x, y):
    matrix = self.board.matrix
    player_index = player.index()
    position = x, y

    for direction_index, direction in enumerate(Cell.DIRECTIONS):
      # Increment each directions of player cell
      points_by_directions = matrix[y][x].points_by_directions
      points_by_directions[direction_index][player_index] += 1

      for way in direction:
        self.update_new_way_weight(player, position, direction_index, way)

  def get_mandatory_moves(self):
    imminent_threats = []
    target_weight = -1
    target_x = 0
    target_y = 0

    for x, row in enumerate(self.board.matrix):
      for y, cell in enumerate(row):
        if not cell.is_free():
          continue
        for points in cell.points_by_directions:
          if points[0] == 4:
            return x, y
          elif points[1] == 4:
            imminent_threats.append([x, y])
        if cell.weight > target_weight:
          target_weight = cell.weight
          target_x = x
          target_y = y
    if imminent_threats:
      return imminent_threats[0]
    return target_x, target_y

  def turn(self):
    # Not implemented yet, just make random move
    board = self.board
    x, y = self.get_mandatory_moves()
    if not x or not y:
      if self.suggested_moves:
        selected_position = random.randint(0, len(self.suggested_moves)-1)
        x, y = list(self.suggested_moves)[selected_position]
      else:
        selected_position = random.randint(0, len(board.avaible_positions)-1)
        x, y = board.avaible_positions[selected_position]

    self.make_move(x, y)
    return x, y