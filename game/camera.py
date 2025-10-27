from __future__ import annotations

from ursina import Entity, Vec3, camera


class FollowCamera:
    """Cinematic follow camera with smoothing and zoom."""

    def __init__(self, target: Entity, offset: Vec3 | None = None) -> None:
        self.target = target
        self.offset = offset or Vec3(0, 6, -12)
        self.zoom = 0.0
        self.sensitivity = 0.3
        self.min_distance = 6.0
        self.max_distance = 18.0
        camera.parent = None
        camera.rotation_x = 18
        camera.rotation_y = 0
        camera.position = self.target.position + self.offset

    def update(self, dt: float) -> None:
        desired = self.target.position + self.offset
        camera.position = camera.position.lerp(desired, min(1, dt * 4.5))
        camera.look_at(self.target.position + Vec3(0, 1.6, 0))

    def adjust_zoom(self, delta: float) -> None:
        self.zoom = max(-1.0, min(1.0, self.zoom + delta * self.sensitivity))
        distance = self.offset.length()
        target_distance = max(self.min_distance, min(self.max_distance, distance - self.zoom * 2.5))
        self.offset = self.offset.normalized() * target_distance
