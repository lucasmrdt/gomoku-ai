#!/usr/bin/env python3
import traceback
import threading

from board import Board, Player
from brain import Brain
from protocol import Protocol
from utils import singleton
from settings import DEBUG_MODE
from abstract import AGame

@singleton
class Gomoku(AGame):
  def __init__(self):
    self.is_running = False
    self.board = Board()
    self.brain = Brain(self.board)
    self.protocol = Protocol(self)
    self.informations = dict()

  def start(self):
    self.is_running = True

    while self.is_running:
      self.protocol.launch_next_command()

  def stop(self):
    self.is_running = False

if __name__ == '__main__':
    if DEBUG_MODE:
      from debug import Debug
      threading.Thread(target=Gomoku.start).start()
      Debug(Gomoku).start()
    else:
      Gomoku.start()
