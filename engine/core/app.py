from __future__ import annotations

import pygame as pg

from ..render.framebuffer import FrameBuffer
from ..render.pipeline import ShaderPipeline
from .clock import Clock
from .errors import SceneError
from .loop import run as run_loop
from .scene import Scene


class App:
    def __init__(
        self,
        *,
        title: str = "Game",
        virtual_width: int = 256,
        virtual_height: int = 224,
        window_scale: int = 4,
        shader_vertex: str,
        shader_fragment: str,
        target_fps: int = 60,
        max_dt: float = 1.0 / 30.0,
        audio=None,
        hud=None,
    ):
        pg.mixer.pre_init(22050, -16, 1, 512)
        pg.init()

        pg.display.set_caption(title)
        pg.display.set_mode(
            (virtual_width * window_scale, virtual_height * window_scale),
            pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE,
            vsync=1,
        )

        self.framebuffer = FrameBuffer(virtual_width, virtual_height)
        self.pipeline = ShaderPipeline(virtual_width, virtual_height, shader_vertex, shader_fragment)
        self.clock = Clock(target_fps, max_dt)

        self.audio = audio
        self.hud = hud

        self.scenes: dict[str, Scene] = {}
        self.scene: Scene | None = None

        self.crt_on = True
        self.aberracao = 0.0
        self.perigo = 0.0

        self.running = True

    def register_scene(self, name: str, scene: Scene) -> None:
        if name in self.scenes:
            raise SceneError(f"cena duplicada: {name!r}")
        self.scenes[name] = scene

    def change_scene(self, name: str) -> None:
        if name not in self.scenes:
            raise SceneError(f"cena não registrada: {name!r}")

        if self.scene is not None:
            self.scene.exit()

        self.scene = self.scenes[name]
        self.scene.enter()

    def stop(self) -> None:
        self.running = False

    def frame(self, dt: float) -> None:
        self.aberracao = 0.0
        self.perigo = 0.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.stop()
            elif event.type == pg.KEYDOWN and event.key == pg.K_m and self.audio is not None:
                self.audio.alternar_mudo()
            elif self.scene is not None:
                self.scene.handle_event(event)

        if self.scene is not None:
            self.scene.update(dt)
            self.scene.draw(self.framebuffer.surface)

        self.pipeline.render(
            self.framebuffer.surface,
            u_crt=1.0 if self.crt_on else 0.0,
            u_aberracao=float(self.aberracao),
            u_perigo=float(self.perigo),
        )

    def run(self) -> None:
        run_loop(self, self.clock)
        pg.quit()
