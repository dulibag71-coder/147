from __future__ import annotations

from ursina import color

WINDOW_SIZE = (1280, 720)
ARENA_SIZE = 32

PLAYER_SPEED = 6.0
SPRINT_MULTIPLIER = 1.6
PLAYER_ROTATION_SPEED = 90.0
PLAYER_MAX_HEALTH = 120.0
PLAYER_ATTACK_COOLDOWN = 0.8
PLAYER_ATTACK_RANGE = 3.0
PLAYER_ATTACK_ARC = 0.75  # cosine threshold for angle check
PLAYER_MELEE_DAMAGE = 18.0

SAFER_ORBIT_DISTANCE = 3.5
SAFER_VERTICAL_OFFSET = 1.6
SAFER_ATTACK_INTERVAL = 4.0
SAFER_ATTACK_RANGE = 12.0
SAFER_SHOT_DAMAGE = 12.0
SAFER_SUPPORT_INTERVAL = 10.0
SAFER_SUPPORT_AMOUNT = 12.0

STAT_MAX = 100.0
STAT_DECAY_PER_MINUTE = {
    "oxygen": 8.0,
    "energy": 5.0,
    "temperature": 4.0,
    "nutrition": 3.5,
}
STAT_CRITICAL_THRESHOLD = 20.0
STAT_DAMAGE_PER_SECOND = 6.0

RESOURCE_KINDS = {
    "scrap": {
        "color": color.rgb(140, 140, 160),
        "value": 2,
    },
    "oxygen": {
        "color": color.azure,
        "restore": {"oxygen": 25.0},
    },
    "energy": {
        "color": color.orange,
        "restore": {"energy": 25.0},
    },
    "nutrition": {
        "color": color.lime,
        "restore": {"nutrition": 25.0},
    },
    "temperature": {
        "color": color.cyan,
        "restore": {"temperature": 25.0},
    },
}

CRAFTING_RECIPES = {
    "충전 배터리": {
        "requirements": {"scrap": 4},
        "effects": {"energy": 35.0},
        "description": "에너지 +35 회복",
    },
    "응급 산소통": {
        "requirements": {"scrap": 3},
        "effects": {"oxygen": 35.0},
        "description": "산소 +35 회복",
    },
    "열선 히터": {
        "requirements": {"scrap": 5},
        "effects": {"temperature": 40.0},
        "description": "체온 +40 회복",
    },
    "영양팩": {
        "requirements": {"scrap": 2},
        "effects": {"nutrition": 30.0},
        "description": "영양 +30 회복",
    },
}

ENEMY_SPAWN_INTERVAL = 12.0
RESOURCE_SPAWN_INTERVAL = 8.0
MAX_ENEMIES = 6
MAX_RESOURCES = 10

HUD_FONT_SIZE = 18
HUD_MESSAGE_DURATION = 5.0
