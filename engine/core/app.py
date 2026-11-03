"""Orquestrador: janela, framebuffer, pipeline, clock, cenas."""

from __future__ import annotations

import pygame as pg

from game.config.settings import GameSettings

from ..render.framebuffer import FrameBuffer
from ..render.pipeline import ShaderPipeline
from .clock import Clock
from .loop import run as run_loop
from .scene_manager import SceneManager


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

        self.title = title
        self.virtual_width = virtual_width
        self.virtual_height = virtual_height
        self.window_scale = window_scale
        self.shader_vertex = shader_vertex
        self.shader_fragment = shader_fragment

        self.settings = GameSettings()

        pg.display.set_caption(self.title)
        self._criar_janela()

        self.framebuffer = FrameBuffer(virtual_width, virtual_height)
        self.pipeline = ShaderPipeline(virtual_width, virtual_height, shader_vertex, shader_fragment)

        self.clock = Clock(self.settings.fps_limit_value if self.settings.fps_limit_value > 0 else target_fps, max_dt)

        self.audio = audio
        self.hud = hud
        self.seed = ""

        self.scene_manager = SceneManager(fallback_name="MENU")

        self.aberracao = 0.0
        self.perigo = 0.0
        self.glitch = 0.0

        self.running = True

    def _criar_janela(self) -> None:
        flags = pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE
        vsync_val = 1 if self.settings.vsync else 0
        w = self.virtual_width * self.window_scale
        h = self.virtual_height * self.window_scale

        pg.display.set_mode((w, h), flags, vsync=vsync_val)

    def apply_video_settings(self) -> None:
        self.clock.target_fps = self.settings.fps_limit_value

        self._criar_janela()

        try:
            self.pipeline = ShaderPipeline(
                self.virtual_width, self.virtual_height, self.shader_vertex, self.shader_fragment
            )
        except Exception as e:
            print(f"[Erro] Não foi possível recriar o pipeline OpenGL: {e}")

    def stop(self) -> None:
        self.running = False

    def frame(self, dt: float) -> None:
        self.aberracao = 0.0
        self.perigo = 0.0
        self.glitch = 0.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.stop()
            elif event.type == pg.KEYDOWN and event.key == pg.K_m and self.audio is not None:
                self.audio.alternar_mudo()
            else:
                self.scene_manager.handle_event(event)

        self.scene_manager.update(dt)
        self.scene_manager.draw(self.framebuffer.surface)

        self.pipeline.render(
            self.framebuffer.surface,
            u_crt=1.0 if self.settings.crt_on else 0.0,
            u_aberracao=float(self.aberracao),
            u_perigo=float(self.perigo),
            u_glitch=float(self.glitch),
        )

    def run(self) -> None:
        run_loop(self, self.clock)
        pg.quit()
