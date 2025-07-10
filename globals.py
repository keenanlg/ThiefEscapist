from pygame.time import Clock

# Global Constants
FPS = 20
CAMERA_SCALE = 3
TILE_SIZE = 16 # 16 pixels
SCALE = 4 # Turn 16x16 to 64x64
SCREEN_WIDTH = TILE_SIZE * 30 # Used to be 480 px
SCREEN_HEIGHT = TILE_SIZE * 20 # Used to be 320 px
HOUSE_WIDTH = TILE_SIZE * 120
HOUSE_HEIGHT = TILE_SIZE * 80

# Flags
paused = False
game_started = False

# Global Clock
clock = Clock()

# Keep track of already looted objects
looted_objects = {}
looted_objects_id = []

# Keep track of exit door info
exit_door_data = {}
exit_door_disabled_time = None