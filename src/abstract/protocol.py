from abc import ABC, abstractmethod

class AProtocol(ABC):
  @abstractmethod
  def launch_next_command(self):
    raise NotImplementedError()
