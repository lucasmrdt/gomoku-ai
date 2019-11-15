import websockets
import asyncio
import json

from protocol import IO
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

  async def _send_matrix(self, ws):
    data = [[cell.dump() for cell in row] for row in self.game.board.matrix]
    await ws.send(json.dumps(data))

  def _on_move(self, ws, data):
    try:
      x, y, player, ai = data['x'], data['y'], data['player'], data['ai']
    except KeyError:
      IO.write_error('error in the incoming request')
      return

    if ai:
      self.game.board.move_player(Player.OPPONENT, x, y)
      self.game.brain.turn()
    else:
      self.game.board.move_player(Player(player), x, y)

  async def listen(self, ws, path):
    self.game.board.reset()
    await self._send_matrix(ws)

    try:
      async for message in ws:
        data = json.loads(message)
        self._on_move(ws, data)
        await self._send_matrix(ws)
    except websockets.WebSocketException:
      IO.write_error(f'websocket has ended unexpectedly')
