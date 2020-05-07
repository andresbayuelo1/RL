import pygame
WIN_VALUE = 2048

GRID_SIZE = 4
SCREEN_SIZE = 600
GRID_SCREEN_SIZE = 500
TILE_SCALING_FACTOR = .9

TILE_SIZE = int(GRID_SCREEN_SIZE / GRID_SIZE)
TILE_LENGTH = TILE_SIZE * TILE_SCALING_FACTOR
TILE_MARGIN = (TILE_SIZE - TILE_LENGTH) / 2


game_actions = {pygame.K_w    : 'up',
                pygame.K_UP   : 'up',

                pygame.K_a    : 'left',
                pygame.K_LEFT : 'left',

                pygame.K_s    : 'down',
                pygame.K_DOWN : 'down',

                pygame.K_d    : 'right', 
                pygame.K_RIGHT: 'right'}

COLORS = {'2':    (228,228,218),
          '4':    (237,224,200),
          '8':    (247,142, 72),
          '16':   (252, 94, 46),
          '32':   (255, 51, 51),
          '64':   (255, 0,  0 ),
          '128':  (237,207,114),
          '256':  (237, 204, 97),
          '512':  (237, 200, 80),
          '1024': (237, 197, 63, 0.47619),
          '2048': (237, 194, 46, 0.55),
          '4096': (237, 146, 46, .77)
          }
BLACK = (0,0,0)