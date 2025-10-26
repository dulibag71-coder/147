import pygame

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
FPS = 60

# Survival stat configuration
STAT_MAX = 100
STAT_DEPLETION_RATES = {
    "oxygen": 6.0,    # per minute
    "energy": 4.5,
    "temperature": 3.5,
    "nutrition": 5.5,
}

STAT_CRITICAL_THRESHOLD = 20
STAT_DAMAGE_PER_SECOND = 8

PLAYER_SPEED = 200  # pixels per second
PLAYER_ATTACK_COOLDOWN = 0.6
PLAYER_ATTACK_RANGE = 60
PLAYER_ATTACK_DAMAGE = 25
PLAYER_MAX_HEALTH = 100

ENEMY_SPEED = 90
ENEMY_DAMAGE = 10
ENEMY_ATTACK_COOLDOWN = 1.2
ENEMY_SPAWN_INTERVAL = 12  # seconds
ENEMY_HEALTH = 60

SAFER_SPEED = 160
SAFER_SUPPORT_INTERVAL = 10
SAFER_HEAL_AMOUNT = 12
SAFER_SHOT_COOLDOWN = 2.5
SAFER_SHOT_DAMAGE = 12
SAFER_SHOT_RANGE = 220

RESOURCE_RESPAWN_INTERVAL = 18
RESOURCE_TYPES = {
    "scrap": {
        "color": (160, 160, 160),
        "amount": 1,
    },
    "oxygen": {
        "color": (120, 200, 255),
        "amount": 25,
    },
    "nutrition": {
        "color": (255, 190, 120),
        "amount": 25,
    },
    "energy": {
        "color": (120, 255, 160),
        "amount": 25,
    },
}

FONT_NAME = "freesansbold.ttf"
BACKGROUND_COLOR = (10, 15, 25)
GRID_COLOR = (30, 40, 55)

pygame.mixer.pre_init(44100, -16, 2, 512)
