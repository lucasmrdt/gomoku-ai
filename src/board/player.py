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

  def isSomeone(self):
    return self.value & SOMEONE

  def isNobody(self):
    return self.value & NOBODY

  def index(self):
    return 0 if self.value == ME else 1

  def opponent_index(self):
    return not self.index()

  def __str__(self):
    if self.value == ME:
      return 'X'
    if self.value == OPPONENT:
      return 'O'
    return '.'
