import re

from .constants import INPUT_STREAM, OUTPUT_STREAM, ERROR_STREAM #IO
from .constants import COMMAND_SPLITTER, RETURN_LINE #Commands
from utils.decorators import singleton

@singleton
class IO():
  BATCH_SIZE = 256

  buffer = ''

  def __read_until(self, end):
    while True:
      match = re.search(end, self.buffer)
      if not match:
        self.buffer += INPUT_STREAM.readline()
      else:
        break
    begin_index, end_index = match.start(), match.end()
    read, rest = self.buffer[:begin_index], self.buffer[end_index:]
    self.buffer = rest
    return read

  def write_error(self, message):
    ERROR_STREAM.write(f'{message}\n')
    ERROR_STREAM.flush()

  def write_standard(self, string):
    OUTPUT_STREAM.write(f'{string}\n')
    OUTPUT_STREAM.flush()

  def get_next_command(self):
    return self.__read_until(COMMAND_SPLITTER).strip()

  def get_params(self, end=RETURN_LINE):
    return self.__read_until(end).strip()
