from __future__ import annotations

import random
from typing import List

from ursina import Sky, Vec3, camera, scene

from . import settings
from .camera import FollowCamera
from .crafting import CraftingSystem
from .enemy import EnemyBase, PurgeDrone, WardenSentinel
from .environment import DayNightCycle, WeatherController
from .hud import HUD
from .missions import MissionLog
from .player import Player
from .resources import ResourceNode
from .safer import Safer
from .world import RuinWorld


class GameState:
    def __init__(self) -> None:
        self.world = RuinWorld()
        self.player = Player()
        self.player.position = Vec3(0, 1.2, -6)
        self.camera = FollowCamera(self.player)
        self.safer = Safer(self.player)
        self.enemies: List[EnemyBase] = []
        self.resources: List[ResourceNode] = []
        self.crafting = CraftingSystem(self.player)
        self.missions = MissionLog()
        self.hud = HUD(self.player, self.missions)
        self.enemy_timer = settings.ENEMY_SPAWN_INTERVAL
        self.resource_timer = settings.RESOURCE_SPAWN_INTERVAL
        self.sky = Sky(color=(0.05, 0.05, 0.08, 1))
        self.day_night = DayNightCycle()
        self.weather = WeatherController()
        self.game_over_reported = False
        self.statistics = {"scrap": 0, "enemies_defeated": 0}
        for _ in range(6):
            self.spawn_resource()
        self.hud.add_message("세이퍼가 온라인 상태입니다")
        self.hud.add_message("[좌클릭] 근접 / [우클릭] 사격 / [G] 채집 / [C] 제작 / [V] 대시 / [F1~F3] 스킬")

    def update(self, dt: float) -> None:
        if not self.player.is_alive():
            if not self.game_over_reported:
                self.hud.add_message("로그가 전투 불능 상태입니다")
                self.game_over_reported = True
            return
        self.player.update(dt)
        self.camera.update(dt)
        self.safer.update(dt, self.enemies)
        for enemy in list(self.enemies):
            if not enemy.enabled:
                continue
            enemy.update(dt, self.player)
            if not enemy.is_alive():
                self._on_enemy_defeated(enemy)
        self._update_survival(dt)
        self._spawn_logic(dt)
        self._update_environment(dt)
        self.statistics["scrap"] = self.player.inventory.stack_count("scrap")
        rewards = self.missions.complete_active(self.statistics)
        if rewards:
            for kind, amount in rewards.items():
                if kind == "experience":
                    for notice in self.player.gain_experience(amount):
                        self.hud.add_message(notice)
                else:
                    self.player.add_resource(kind, amount)
                    if kind == "scrap":
                        self.statistics["scrap"] = self.player.inventory.stack_count("scrap")
            self.hud.add_message("임무 완료")
        env_text = f"{self.weather.current.upper()} | 적 {len(self.enemies)}/{settings.MAX_ENEMIES}"
        self.hud.update(dt, self.statistics, env_text)

    def _update_environment(self, dt: float) -> None:
        self.day_night.update(dt)
        tint, density = self.weather.update(dt)
        camera.clip_plane_near = 0.3
        camera.clip_plane_far = 120
        scene.fog_color = tint
        scene.fog_density = density

    def _update_survival(self, dt: float) -> None:
        if self.player.health <= 0:
            return
        stats = self.player.stats.as_dict()
        for stat, value in stats.items():
            if value <= 0:
                self.player.take_damage(settings.STAT_DAMAGE_PER_SECOND * dt)
        if self.player.health <= 0:
            self.hud.add_message("생존 실패")

    def _spawn_logic(self, dt: float) -> None:
        self.enemy_timer -= dt
        if self.enemy_timer <= 0 and len(self.enemies) < settings.MAX_ENEMIES:
            self.spawn_enemy()
            self.enemy_timer = settings.ENEMY_SPAWN_INTERVAL
        self.resource_timer -= dt
        if self.resource_timer <= 0 and len(self.resources) < settings.MAX_RESOURCES:
            self.spawn_resource()
            self.resource_timer = settings.RESOURCE_SPAWN_INTERVAL

    def spawn_enemy(self) -> None:
        if random.random() < 0.15 and all(not isinstance(enemy, WardenSentinel) for enemy in self.enemies):
            enemy = WardenSentinel(Vec3(random.uniform(-5, 5), 0.7, random.uniform(-5, 5)))
            self.hud.add_message("감시자 파편 등장")
        else:
            enemy = PurgeDrone.random_spawn()
            self.hud.add_message("정화 드론 접근")
        self.enemies.append(enemy)

    def spawn_resource(self) -> None:
        node = ResourceNode.random()
        self.resources.append(node)

    def handle_attack(self) -> None:
        target = self.player.perform_attack(self.enemies)
        if target:
            if not target.is_alive():
                self._on_enemy_defeated(target)
            else:
                self.hud.add_message("적에게 피해를 입혔습니다")
        else:
            self.hud.add_message("공격 범위에 적이 없습니다")

    def handle_ranged(self) -> None:
        target = self.player.perform_ranged(self.enemies)
        if target:
            if not target.is_alive():
                self._on_enemy_defeated(target)
            self.hud.add_message("원거리 사격 성공")
        else:
            self.hud.add_message("조준할 대상이 없습니다")

    def _on_enemy_defeated(self, enemy: EnemyBase) -> None:
        if enemy in self.enemies:
            self.enemies.remove(enemy)
        enemy.disable()
        loot = enemy.loot_table()
        for kind, amount in loot.items():
            self.player.add_resource(kind, amount)
            if kind == "scrap":
                self.statistics["scrap"] = self.player.inventory.stack_count("scrap")
        self.statistics["enemies_defeated"] += 1
        self.hud.add_message("위협 제거")
        for notice in self.player.gain_experience(45):
            self.hud.add_message(notice)

    def handle_resource_gather(self) -> None:
        closest = None
        closest_distance = 2.0
        for node in list(self.resources):
            distance = (node.position - self.player.position).length()
            if distance < closest_distance:
                closest = node
                closest_distance = distance
        if closest:
            message = closest.gather(self.player)
            if closest.kind == "scrap":
                self.statistics["scrap"] = self.player.inventory.stack_count("scrap")
            closest.disable()
            self.resources.remove(closest)
            self.hud.add_message(message)
        else:
            self.hud.add_message("채집 가능한 자원이 근처에 없습니다")

    def handle_crafting_toggle(self) -> None:
        active = self.crafting.toggle()
        if active:
            recipes = self.crafting.available_recipes()
            self.hud.show_crafting(recipes.keys())
            if not recipes:
                self.hud.add_message("사용 가능한 제작이 없습니다")
        else:
            self.hud.hide_crafting()

    def handle_craft_selection(self, index: int) -> None:
        recipes = list(self.crafting.available_recipes().keys())
        if 0 <= index < len(recipes):
            result = self.crafting.craft(recipes[index])
            self.hud.add_message(result)
            self.hud.hide_crafting()
            self.crafting.active = False
            self.statistics["scrap"] = self.player.inventory.stack_count("scrap")
        else:
            self.hud.add_message("선택할 수 없는 제작 번호")

    def handle_dash(self) -> None:
        if self.player.dash():
            self.hud.add_message("전술 이동")

    def handle_skill_unlock(self, index: int) -> None:
        names = list(self.player.skills.skills.keys())
        if 0 <= index < len(names):
            result = self.player.skills.unlock(names[index])
            self.hud.add_message(result)
        else:
            self.hud.add_message("스킬을 선택할 수 없습니다")

    def reset(self) -> None:
        for enemy in self.enemies:
            enemy.disable()
        for node in self.resources:
            node.disable()
        self.safer.disable()
        self.player.disable()
        self.hud.destroy()
        self.world.ground.disable()
        for structure in self.world.structures:
            structure.disable()
        self.world.landing_pad.disable()
        self.sky.disable()
        self.day_night.sun.disable()
        self.day_night.ambient.disable()
        self.__init__()
