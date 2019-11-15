BRAIN_NAME  = "I've already won 💪🏻"
VERSION     = "1.0"
AUTHOR      = "Marandat and Desfonds"
COUNTRY     = "FR"

INFORMATIONS = {
  'name': BRAIN_NAME,
  'version': VERSION,
  'author': AUTHOR,
  'country': COUNTRY
}

# Debug
try:
  import websockets
  DEBUG_MODE = True
except ImportError:
  DEBUG_MODE = False
DEBUG_PORT = 1234

DEFAULT_BOARD_SIZE = 19
