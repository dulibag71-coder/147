from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from ursina import Entity, load_model

from . import settings


class AssetLibrary:
    """Runtime loader that prefers Blender-exported assets when available."""

    def __init__(self, root: str | Path = "") -> None:
        self.root = Path(root) if root else Path.cwd()
        self._cache: Dict[str, Optional[str]] = {}

    def resolve_model(self, key: str) -> Optional[str]:
        if key in self._cache:
            return self._cache[key]
        path = settings.ASSET_PATHS.get(key)
        if path:
            candidate = self.root / path
            if candidate.exists():
                try:
                    load_model(candidate.as_posix(), use_deepcopy=True)
                except Exception:  # pragma: no cover - fallback will be used
                    self._cache[key] = settings.FALLBACK_MODELS.get(key)
                else:
                    self._cache[key] = candidate.as_posix()
                    return self._cache[key]
        self._cache[key] = settings.FALLBACK_MODELS.get(key)
        return self._cache[key]

    def spawn(self, key: str, **kwargs) -> Entity:
        model = self.resolve_model(key)
        if model:
            kwargs.setdefault("model", model)
        return Entity(**kwargs)


ASSETS = AssetLibrary()
