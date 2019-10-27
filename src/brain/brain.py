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

  def get_point_from_way(self, position, direction_index, way):
    # Take the current cell
    x, y = position
    cell = self.board.matrix[y][x]
    cell_points = cell.points_by_directions[direction_index]

    # Take the neighbour cell from the direction
    neighbour_x, neighbour_y = map(operator.add, position, way)
    if not self.board.is_valid_coordinate(neighbour_x, neighbour_y):
      return 0
    neighbour_cell = self.board.matrix[neighbour_y][neighbour_x]

    # Get the neighbour owner
    my = neighbour_cell.owner if neighbour_cell.owner != Player.NOBODY else cell.owner

    # Get the neighbour_owner value and her opponent value to.
    my_value = cell_points[my.index()]
    opponent_value = cell_points[my.opponent_index()]

    # Dispatched value is by default the current value
    point = my_value

    # If their is no opponent next to current cell, we increment the lenght of the threat
    if opponent_value == 0:
      point += 1

    # If the move is made by the opponent, position is now closed so we decrement point
    if my != cell.owner:
      point -= 1

    return point

  def update_new_way_point(self, default_player, position, direction_index, way):
    player = None
    board_size = self.board.size
    matrix = self.board.matrix
    point = self.get_point_from_way(position, direction_index, way)

    while True:
      position = tuple(map(operator.add, position, way))
      x, y = position
      # If position is outside the board we stop propagate new way value.
      if not self.board.is_valid_coordinate(x, y):
        break

      cell = matrix[y][x]

      # We need to track in which player we propagate the new way value.
      if not player:
        player = cell.owner if cell.owner != Player.NOBODY else default_player

      # If we found an different player that the first met, we stop propagate the new way value.
      if cell.owner != player:
        if cell.is_free():
          cell.points_by_directions[direction_index][player.index()] = point
          cell.compute_weight()
        break

      cell.points_by_directions[direction_index][player.index()] = point
      cell.compute_weight()


  def on_player_move(self, player, x, y):
    matrix = self.board.matrix
    player_index = player.index()
    position = x, y

    for direction_index, direction in enumerate(Cell.DIRECTIONS):
      for way in direction:
        self.update_new_way_point(player, position, direction_index, way)

      # Increment each directions of player cell
      points_by_directions = matrix[y][x].points_by_directions
      points_by_directions[direction_index][player_index] += 1


  def get_mandatory_moves(self):
    imminent_threats = []
    target_weight = -1
    target_x = 0
    target_y = 0

    for y, row in enumerate(self.board.matrix):
      for x, cell in enumerate(row):
        if not cell.is_free():
          continue
        for points in cell.points_by_directions:
          if points[1] >= 3:
            return x, y
          elif points[0] >= 3:
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