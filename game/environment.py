from __future__ import annotations

import itertools
import math
import random
from typing import Iterator

from ursina import AmbientLight, DirectionalLight, Vec3, color

from . import settings


class DayNightCycle:
    def __init__(self) -> None:
        self.timer = 0.0
        self.length = settings.DAY_LENGTH_SECONDS
        self.ambient = AmbientLight(color=color.rgb(60, 60, 80))
        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1, -1, 1))

    def update(self, dt: float) -> None:
        self.timer = (self.timer + dt) % self.length
        phase = self.timer / self.length
        sun_height = max(0.0, math.sin(phase * math.tau))
        intensity = 0.25 + 0.75 * sun_height
        daylight = color.rgb(160, 180, 210)
        dusk = color.rgb(110, 90, 120)
        night = color.rgb(40, 50, 80)
        if phase < 0.4:
            ratio = phase / 0.4
            tint = dusk.lerp(daylight, ratio)
        elif phase < 0.7:
            ratio = (phase - 0.4) / 0.3
            tint = daylight.lerp(dusk, ratio)
        else:
            ratio = (phase - 0.7) / 0.3
            tint = dusk.lerp(night, ratio)
        self.sun.color = tint
        self.ambient.color = tint * intensity
        self.sun.rotation_x = -90 + 180 * phase


class WeatherController:
    def __init__(self) -> None:
        self.timer = 0.0
        self.current = "clear"
        self.sequence: Iterator[str] = itertools.cycle(settings.FOG_SETTINGS.keys())

    def update(self, dt: float) -> tuple[color.Color, float]:
        self.timer += dt
        if self.timer >= settings.WEATHER_TRANSITION_SECONDS:
            self.timer = 0.0
            self.current = next(self.sequence)
        tint, density = settings.FOG_SETTINGS[self.current]
        jitter = random.uniform(-0.01, 0.01)
        return tint, max(0.0, density + jitter)
