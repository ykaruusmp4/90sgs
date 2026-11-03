from dataclasses import dataclass


@dataclass
class GameSettings:
    difficulty: int = 1
    map_size: int = 48
    crt_on: bool = True
    multithread: bool = False
    vsync: bool = False
    fps_limit_idx: int = 0

    @property
    def difficulty_name(self) -> str:
        return ["EASY", "NORMAL", "HARD"][self.difficulty]

    @property
    def map_size_name(self) -> str:
        return ["SMALL", "MEDIUM", "LARGE"][[32, 48, 64].index(self.map_size)]

    @property
    def fps_limit_name(self) -> str:
        return ["UNLTD", "60", "120", "144", "240"][self.fps_limit_idx]

    @property
    def fps_limit_value(self) -> int:
        return [0, 60, 120, 144, 240][self.fps_limit_idx]

    @property
    def speed_mult(self) -> float:
        return [0.6, 1.0, 1.35][self.difficulty]

    @property
    def time_mult(self) -> float:
        return [1.5, 1.0, 0.7][self.difficulty]

    @property
    def monster_delay(self) -> float:
        return [8.0, 4.5, 2.0][self.difficulty]
