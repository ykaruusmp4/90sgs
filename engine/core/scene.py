"""Base de cena. Todos os métodos são no-op por default — sobrescreva só o que
precisar. `enter`/`exit` são chamados por `App.change_scene` (útil pra ligar
ambiente sonoro e preparar estado sem colocar lógica no construtor).
"""

from __future__ import annotations

import pygame as pg


class Scene:
    __slots__ = ("app",)

    def __init__(self, app):
        self.app = app

    def enter(self) -> None:
        """Chamado ao entrar na cena (logo antes do primeiro update/draw)."""

    def exit(self) -> None:
        """Chamado ao sair (antes de `enter` da próxima cena)."""

    def handle_event(self, event: pg.event.Event) -> None:
        """Um evento pygame por chamada. Scene decide se ignora, consome ou repassa."""

    def update(self, dt: float) -> None:
        """Física/lógica. `dt` em segundos, já clampado pelo Clock."""

    def draw(self, surface: pg.Surface) -> None:
        """Desenha sobre a surface virtual do framebuffer."""
