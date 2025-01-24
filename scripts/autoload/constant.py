import pygame
import math

from pygame.math import Vector2
from pygame.time import get_ticks


#   Display
DISPLAY_WIDTH, DISPLAY_HEIGHT, DISPLAY_FLAGS = 960, 800, pygame.SCALED | pygame.RESIZABLE
DISPLAY_TITLE = "Arc Dash"

#   Color
WHITE, BLACK = pygame.Color(255, 255, 255, 255), pygame.Color(0, 0, 0, 0)

#   Color (Gradient)
MENU_MAIN_TOP, MENU_MAIN_BOT = pygame.Color(245, 245, 245), pygame.Color(200, 74, 238)
MENU_MAIN_BAND = 32

MENU_PLAY_TOP, MENU_PLAY_BOT = pygame.Color(73, 231, 236), pygame.Color(171, 31, 101)
MENU_PLAY_BAND = 12

#   Color (Menu)
MENU_MAIN_BUTTON_COLOR = pygame.Color(0, 0, 0, 55)
MENU_PLAY_WIN_TIME = 5000

#   Color (Hud)
HUD_NAMETAG_COLOR = pygame.Color(244, 196, 48)
HUD_SCOREBOARD_COLOR = pygame.Color(255, 53, 3)
HUD_WIN_OVERLAY_COLOR = pygame.Color(0, 0, 0, 128)

HUD_OUTLINE_COLOR = pygame.Color(0, 0, 0)

#   Entity
ENTITY_ACCELERATION = 0.58

ENTITY_FRICTION = 0.12
ENTITY_GRAVITY = 0.24

ENTITY_JUMP_FORCE = 7.2
ENTITY_JUMP_AMOUNT = 2

ENTITY_SKIP_FORCE = 1.2
ENTITY_SKIP_TIME = 50

ENTITY_HURT_COLOR = pygame.Color(210, 47, 30, 255)
ENTITY_HURT_OUTLINE_COLOR = pygame.Color(0, 0, 0)
ENTITY_HURT_TIME = 150

#   Entity (Player)
PLAYER_RESPAWN_POSITION = (DISPLAY_WIDTH / 2, -DISPLAY_HEIGHT / 4)
PLAYER_RESPAWN_TIME = 1000

PLAYER_HURTBOX_OFFSET = {"biker": (-4, -4), "punk": (-2, -2), "cyborg": (0, 0)}

#   Animation
ANIMATION_SPEED = 8

#   Object (Tile)
TILE_SIZE = 32
TILE_TOLERANCE = 5

#   Object (Hand)
HAND_DIRECTION = {"down": {"frame": 0, "rotation": -90},
                  "half_down": {"frame": 1, "rotation": -45},
                  "straight": {"frame": 2, "rotation": 0},
                  "half_up": {"frame": 3, "rotation": 45},
                  "up": {"frame": 4, "rotation": 90}
                  }

HAND_OFFSET = {"biker_hand": (0, -4), "punk_hand": (-2, -2), "cyborg_hand": (-2, -6)}

BASE_AIM_THRESHOLD = math.pi / 8

DISTANCE_AIM_CLOSE = 1.0
DISTANCE_AIM_FAR = 200

#   Object (Pistol)
PISTOL_DIRECTION = {
    "pulse_blaster": {
        "down": {"offset": (4, 11), "muzzle": (2, 6)},
        "half_down": {"offset": (10, 6), "muzzle": (5, 3)},
        "straight": {"offset": (12, -3), "muzzle": (6, -1)},
        "half_up": {"offset": (6, -10), "muzzle": (3, -5)},
        "up": {"offset": (0, -11), "muzzle": (-1, -6)}
    },
    "ion_dart": {
        "down": {"offset": (4, 12), "muzzle": (2, 6)},
        "half_down": {"offset": (10, 6), "muzzle": (5, 3)},
        "straight": {"offset": (12, -4), "muzzle": (6, -1)},
        "half_up": {"offset": (6, -10), "muzzle": (3, -5)},
        "up": {"offset": (0, -12), "muzzle": (-1, -6)}
    },
    "electro_bolter": {
        "down": {"offset": (4, 12), "muzzle": (2, 6)},
        "half_down": {"offset": (10, 6), "muzzle": (5, 3)},
        "straight": {"offset": (12, -4), "muzzle": (6, -1)},
        "half_up": {"offset": (6, -10), "muzzle": (3, -5)},
        "up": {"offset": (0, -12), "muzzle": (-1, -6)}
    }
}

#   Object (Bullet)
BULLET_STATS = {"pulse_blaster_projectile": {"speed": 1200, "force": 18.5},
                "ion_dart_projectile": {"speed": 1000, "force": 20},
                "electro_bolter_projectile": {"speed": 1300, "force": 22.5}
                }
BULLET_TIME = 3000

BULLET_HITBOX_OFFSET = (2, 2)

#   Debug (All)
DEBUG = False