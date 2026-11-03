from __future__ import annotations

from .errors import SceneError
from .scene import Scene


class SceneManager:
    __slots__ = ("scenes", "current", "current_name", "fallback_name")

    def __init__(self, fallback_name: str = "MENU"):
        self.scenes: dict[str, Scene] = {}
        self.current: Scene | None = None
        self.current_name: str = ""
        self.fallback_name = fallback_name

    def register(self, name: str, scene: Scene) -> None:
        if name in self.scenes:
            raise SceneError(f"Cena duplicada: {name!r}")
        self.scenes[name] = scene

    def change(self, name: str) -> None:
        if name not in self.scenes:
            print(f"[SceneManager] Aviso: Cena '{name}' não existe. Usando fallback '{self.fallback_name}'.")
            name = self.fallback_name

        if name not in self.scenes:
            raise SceneError(f"Fallback '{self.fallback_name}' também não registrado!")

        if self.current is not None:
            self.current.exit()

        self.current_name = name
        self.current = self.scenes[name]
        self.current.enter()

    def update(self, dt: float) -> None:
        if self.current:
            self.current.update(dt)

    def draw(self, surface) -> None:
        if self.current:
            self.current.draw(surface)

    def handle_event(self, event) -> None:
        if self.current:
            self.current.handle_event(event)
