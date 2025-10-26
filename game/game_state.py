from __future__ import annotations

from typing import List

from ursina import Sky, Vec3, camera

from . import settings
from .crafting import CraftingSystem
from .enemy import PurgeDrone
from .hud import HUD
from .player import Player
from .resources import ResourceNode
from .safer import Safer
from .world import RuinWorld


class GameState:
    def __init__(self) -> None:
        camera.position = Vec3(0, 6, -12)
        camera.rotation_x = 20
        self.world = RuinWorld()
        self.player = Player()
        camera.parent = self.player
        self.player.position = Vec3(0, 1, -6)
        self.safer = Safer(self.player)
        self.enemies: List[PurgeDrone] = []
        self.resources: List[ResourceNode] = []
        self.crafting = CraftingSystem(self.player)
        self.hud = HUD(self.player)
        self.enemy_timer = settings.ENEMY_SPAWN_INTERVAL
        self.resource_timer = settings.RESOURCE_SPAWN_INTERVAL
        self.sky = Sky(color=(0.05, 0.05, 0.08, 1))
        self.game_over_reported = False
        for _ in range(4):
            self.spawn_resource()
        self.hud.add_message("세이퍼가 온라인 상태입니다")
        self.hud.add_message("[마우스 좌클릭] 근접 공격 / [G] 채집 / [C] 제작")

    def update(self, dt: float) -> None:
        if not self.player.is_alive():
            if not self.game_over_reported:
                self.hud.add_message("로그가 전투 불능 상태입니다")
                self.game_over_reported = True
            return
        self.player.update(dt)
        self.safer.update(dt, self.enemies)
        for enemy in list(self.enemies):
            enemy.update(dt, self.player)
            if not enemy.is_alive():
                self.enemies.remove(enemy)
                enemy.disable()
                self.hud.add_message("위협 제거")
        self._update_survival(dt)
        self._spawn_logic(dt)
        self.hud.update(dt)

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
            enemy = PurgeDrone.random_spawn()
            self.enemies.append(enemy)
            self.hud.add_message("정화 드론 접근")
            self.enemy_timer = settings.ENEMY_SPAWN_INTERVAL
        self.resource_timer -= dt
        if self.resource_timer <= 0 and len(self.resources) < settings.MAX_RESOURCES:
            self.spawn_resource()
            self.resource_timer = settings.RESOURCE_SPAWN_INTERVAL

    def spawn_resource(self) -> None:
        node = ResourceNode.random()
        self.resources.append(node)

    def handle_attack(self) -> None:
        target = self.player.perform_attack(self.enemies)
        if target:
            if not target.is_alive():
                self.enemies.remove(target)
                target.disable()
                self.hud.add_message("근접 타격 성공")
            else:
                self.hud.add_message("적에게 피해를 입혔습니다")
        else:
            self.hud.add_message("공격 범위에 적이 없습니다")

    def handle_resource_gather(self) -> None:
        closest = None
        closest_distance = 2.0
        for node in self.resources:
            distance = (node.position - self.player.position).length()
            if distance < closest_distance:
                closest = node
                closest_distance = distance
        if closest:
            message = closest.gather(self.player)
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
        else:
            self.hud.add_message("선택할 수 없는 제작 번호")

    def reset(self) -> None:
        for enemy in self.enemies:
            enemy.disable()
        for node in self.resources:
            node.disable()
        self.safer.disable()
        self.player.disable()
        self.world.ground.disable()
        for structure in self.world.structures:
            structure.disable()
        self.world.landing_pad.disable()
        self.sky.disable()
        self.__init__()
