from enum import Enum

NOBODY    = 0
ME        = 1 << 0
OPPONENT  = 1 << 1
SOMEONE   = ME | OPPONENT

class Player(Enum):
  NOBODY    = NOBODY
  ME        = ME
  OPPONENT  = OPPONENT
  SOMEONE   = SOMEONE

  def is_someone(self):
    return self.value & SOMEONE

  def index(self):
    return 0 if self.value == ME else 1

  def opponent_index(self):
    return not self.index()

  def get_opponent(self):
    return self.OPPONENT if self.value == ME else self.ME

  def __str__(self):
    if self.value == ME:
      return 'X'
    if self.value == OPPONENT:
      return 'O'
    return '.'
