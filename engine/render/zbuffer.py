from __future__ import annotations

INF = 1e30


class ZBuffer:
    __slots__ = ("data",)

    def __init__(self, width: int):
        self.data = [INF] * width

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, i: int) -> float:
        return self.data[i]

    def __setitem__(self, i: int, v: float) -> None:
        self.data[i] = v

    def reset(self) -> None:
        d = self.data
        for i in range(len(d)):
            d[i] = INF
