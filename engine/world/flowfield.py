from collections import deque

from .grid import Grid

DIRS8 = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))


class FlowField:

    def __init__(self, grid: Grid):
        self.grid = grid
        n = grid.n
        self.n = n
        self.vizinhos = [[] for _ in range(n * n)]

        def livre(x, y):
            return 0 <= x < n and 0 <= y < n and not grid.is_solid(x, y)

        for y in range(n):
            for x in range(n):
                if not livre(x, y):
                    continue
                lista = []
                for dx, dy in DIRS8:
                    if not livre(x + dx, y + dy):
                        continue
                    if dx and dy and not (livre(x + dx, y) and livre(x, y + dy)):
                        continue
                    lista.append((y + dy) * n + (x + dx))
                self.vizinhos[y * n + x] = lista

        self.dist = [-1] * (n * n)
        self.origem = -1

    def atualizar(self, cx: int, cy: int):
        idx = cy * self.n + cx
        if idx == self.origem:
            return
        self.origem = idx

        dist = [-1] * len(self.vizinhos)
        dist[idx] = 0
        fila = deque([idx])
        viz = self.vizinhos

        while fila:
            i = fila.popleft()
            d = dist[i] + 1
            for j in viz[i]:
                if dist[j] < 0:
                    dist[j] = d
                    fila.append(j)
        self.dist = dist

    def proximo(self, cx: int, cy: int) -> tuple[int, int] | None:
        i = cy * self.n + cx
        atual = self.dist[i]
        if atual <= 0:
            return None

        melhor, chave = None, None
        for j in self.vizinhos[i]:
            d = self.dist[j]
            if d < 0 or d >= atual:
                continue
            jx, jy = j % self.n, j // self.n
            k = (d, (jx - self.origem % self.n) ** 2 + (jy - self.origem // self.n) ** 2)
            if chave is None or k < chave:
                melhor, chave = (jx, jy), k
        return melhor
