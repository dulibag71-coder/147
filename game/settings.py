from __future__ import annotations

from ursina import color

WINDOW_SIZE = (1600, 900)
ARENA_SIZE = 48

# --- Player locomotion ---
PLAYER_SPEED = 7.2
PLAYER_ACCELERATION = 18.0
PLAYER_DECELERATION = 16.0
SPRINT_MULTIPLIER = 1.75
PLAYER_ROTATION_SPEED = 120.0
PLAYER_MAX_HEALTH = 160.0
PLAYER_SHIELD_MAX = 60.0
PLAYER_SHIELD_RECHARGE_RATE = 5.0
PLAYER_ATTACK_COOLDOWN = 0.65
PLAYER_ATTACK_RANGE = 3.4
PLAYER_ATTACK_ARC = 0.77  # cosine threshold for angle check
PLAYER_MELEE_DAMAGE = 22.0
PLAYER_RANGED_DAMAGE = 16.0
PLAYER_RANGED_INTERVAL = 0.75
PLAYER_AIM_SENSITIVITY = 55.0

# --- Companion configuration ---
SAFER_ORBIT_DISTANCE = 4.2
SAFER_VERTICAL_OFFSET = 1.8
SAFER_ATTACK_INTERVAL = 2.8
SAFER_ATTACK_RANGE = 15.0
SAFER_SHOT_DAMAGE = 18.0
SAFER_SUPPORT_INTERVAL = 8.0
SAFER_SUPPORT_AMOUNT = 14.0
SAFER_REPAIR_AMOUNT = 8.0

# --- Survival stats ---
STAT_MAX = 120.0
STAT_DECAY_PER_MINUTE = {
    "oxygen": 9.0,
    "energy": 6.0,
    "temperature": 5.0,
    "nutrition": 4.2,
}
STAT_CRITICAL_THRESHOLD = 25.0
STAT_DAMAGE_PER_SECOND = 8.0

# --- Progression ---
EXPERIENCE_PER_LEVEL = 250
SKILL_POINTS_PER_LEVEL = 2

# --- Environment ---
DAY_LENGTH_SECONDS = 480.0
WEATHER_TRANSITION_SECONDS = 90.0
FOG_SETTINGS = {
    "clear": (color.rgb(40, 42, 55), 0.01),
    "dust": (color.rgb(120, 90, 60), 0.04),
    "ion": (color.rgb(80, 120, 150), 0.06),
}

# --- Asset management ---
ASSET_PATHS = {
    "player": "assets/models/player.glb",
    "safer": "assets/models/safer.glb",
    "purge_drone": "assets/models/purge_drone.glb",
    "warden": "assets/models/warden.glb",
    "resource_scrap": "assets/models/scrap_crate.glb",
    "resource_canister": "assets/models/canister.glb",
    "landing_pad": "assets/models/landing_pad.glb",
    "structure": "assets/models/structure.glb",
}
FALLBACK_MODELS = {
    "player": "cube",
    "safer": "sphere",
    "purge_drone": "sphere",
    "warden": "cube",
    "resource_scrap": "cube",
    "resource_canister": "cube",
    "landing_pad": "cube",
    "structure": "cube",
}

RESOURCE_KINDS = {
    "scrap": {
        "color": color.rgb(140, 140, 160),
        "value": 4,
    },
    "oxygen": {
        "color": color.azure,
        "restore": {"oxygen": 30.0},
    },
    "energy": {
        "color": color.orange,
        "restore": {"energy": 30.0},
    },
    "nutrition": {
        "color": color.lime,
        "restore": {"nutrition": 35.0},
    },
    "temperature": {
        "color": color.cyan,
        "restore": {"temperature": 35.0},
    },
    "data_chip": {
        "color": color.magenta,
        "value": 1,
    },
}

CRAFTING_RECIPES = {
    "충전 배터리": {
        "requirements": {"scrap": 5},
        "effects": {"energy": 45.0},
        "description": "에너지 +45 회복",
    },
    "응급 산소통": {
        "requirements": {"scrap": 4},
        "effects": {"oxygen": 45.0},
        "description": "산소 +45 회복",
    },
    "열선 히터": {
        "requirements": {"scrap": 6},
        "effects": {"temperature": 55.0},
        "description": "체온 +55 회복",
    },
    "영양팩": {
        "requirements": {"scrap": 4},
        "effects": {"nutrition": 45.0},
        "description": "영양 +45 회복",
    },
    "임시 방어막": {
        "requirements": {"scrap": 6, "data_chip": 1},
        "effects": {"shield": 40.0},
        "description": "방어막 +40 회복",
    },
}

ENEMY_SPAWN_INTERVAL = 9.0
RESOURCE_SPAWN_INTERVAL = 6.0
MAX_ENEMIES = 9
MAX_RESOURCES = 14

HUD_FONT_SIZE = 18
HUD_MESSAGE_DURATION = 5.0

MISSIONS = [
    {
        "id": "tutorial_escape",
        "title": "더미 스테이션 탈출",
        "description": "생존 시스템을 복구하고 탈출 모듈을 확보하라.",
        "requirements": {"scrap": 10},
        "reward": {"experience": 100, "data_chip": 1},
    },
    {
        "id": "colony_signal",
        "title": "왜곡 신호 추적",
        "description": "정화 드론을 처치하여 손상된 데이터 칩을 확보하라.",
        "requirements": {"enemies_defeated": 8},
        "reward": {"experience": 200, "scrap": 6},
    },
]

SKILL_TREE = {
    "전투 프로토콜": {
        "description": "근접 공격력이 12% 증가합니다.",
        "stat": "melee_bonus",
        "value": 0.12,
    },
    "전술 회피": {
        "description": "대시 쿨다운이 20% 감소합니다.",
        "stat": "dash_cooldown",
        "value": -0.2,
    },
    "회복 주입": {
        "description": "아이템 사용 시 체력 10 회복.",
        "stat": "item_heal",
        "value": 10,
    },
}
