import websockets
import asyncio
import json

from board import Player
from settings import DEBUG_PORT
from abstract import AGame

class Debug():
  def __init__(self, game: AGame):
    self.game = game

  def start(self):
    ws = websockets.serve(self.listen, '127.0.0.1', DEBUG_PORT)
    asyncio.get_event_loop().run_until_complete(ws)
    asyncio.get_event_loop().run_forever()

  async def __send_matrix(self, ws):
    data = [[cell.dump() for cell in row] for row in self.game.board.matrix]
    await ws.send(json.dumps(data))

  def __on_move(self, ws, data):
    x, y, player, ia = data['x'], data['y'], data['player'], data['ia']
    if ia:
      self.game.board.move_player(Player.OPPONENT, x, y)
      self.game.brain.turn()
    else:
      self.game.board.move_player(Player(player), x, y)

  async def listen(self, ws, path):
    self.game.board.reset()
    await self.__send_matrix(ws)

    async for message in ws:
      try:
        data = json.loads(message)
        self.__on_move(ws, data)
        await self.__send_matrix(ws)
      except Exception as e:
        print(f'error: {e.message}')
