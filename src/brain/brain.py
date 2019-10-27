import operator
import random

from board import Player, Cell
from abstract import ABrain, ABoard

class Brain(ABrain):
  def __init__(self, board: ABoard):
    board.listen_player_move(self.on_player_make_move)
    self.board = board

  def reset(self):
    self.suggested_moves = set()

  def make_move(self, x: int, y: int):
    self.board.player_move(Player.ME, x, y)

  def compute_new_line_weight(self, default_player, position, direction_information):
    direction_index, direction = direction_information

    # Take the current cell
    x, y = position
    cell = self.board.matrix[y][x]

    # Take the neighbour cell from the direction
    neighbour_x, neighbour_y = map(operator.add, position, direction)
    neighbour_cell = self.board.matrix[neighbour_y][neighbour_x]

    # Get the neighbour owner
    neighbour_owner = neighbour_cell.owner if neighbour_cell.owner != Player.NOBODY else default_player

    # Get the neighbour_owner value and her opponent value to.
    neighbour_value = cell[direction_index][neighbour_owner.index()]
    opponent_value = cell[direction_index][neighbour_owner.opponent_index()]

    # Compute the new line weight
    malus = min(1, opponent_value) # Malus can only be 0 or 1.
    return neighbour_value - malus

  def propagate_new_line_weight(self, x, y, default_player, line_index):
    player = None
    board_size = self.board.size
    matrix = self.board.matrix

    while True:
      if x < 0 or x >= board_size \
      or y < 0 or y >= board_size:
        break

      if not player:
        owner = matrix[y][x].owner
        player = owner if owner != Player.NOBODY else default_player

  def on_player_move(self, player, x, y):
    return
    player_index = player.index()
    board_size = self.board.size
    position = x, y

    for i, line in enumerate(Cell.LINES):
      # Increment
      matrix[y][x][i][player_index] += 1

      # while True:

      # for 

  def mandatory_moves(self):
    imminent_threats = []
    for x, row in enumerate(self.board.matrix):
      for y, cell in enumerate(row):
        for direction in cell:
          if direction.points_by_lines[0] == 4:
            return x, y
          elif direction.points_by_lines[1] == 4:
            imminent_threats.add([x, y])
    if imminent_threats:
      return imminent_threats[0][0], imminent_threats[0][1]
    return None, None

  def turn(self):
    # Not implemented yet, just make random move
    board = self.board
    x, y = mandatory_moves()
    if not x or not y:
      if self.suggested_moves:
        selected_position = random.randint(0, len(self.suggested_moves)-1)
        x, y = list(self.suggested_moves)[selected_position]
      else:
        selected_position = random.randint(0, len(board.avaible_positions)-1)
        x, y = board.avaible_positions[selected_position]

    self.make_move(x, y)
    return x, y