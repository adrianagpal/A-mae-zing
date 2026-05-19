import random
from .high_definitions import MODIFIABLE, BARRIER
from .high_definitions import S, E, OPPOSITE, DIR_DELTA, DIRECTIONS
import numpy.typing as npt
import numpy as np
from typing import Any


def in_bounds(grid: npt.NDArray[np.integer], r: int, c: int) -> bool:
    return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]


def is_modifiable(grid: npt.NDArray[np.integer], r: int, c: int) -> bool:
    return int(grid[r][c]) == MODIFIABLE


"""
Destroys a wall between cells, carving it
"""


def carve(grid: npt.NDArray[Any],
          r1: int, c1: int, r2: int, c2: int, direction: int,) -> bool:

    if grid[r1][c1] == BARRIER or grid[r2][c2] == BARRIER:
        return False

    grid[r1][c1] &= ~direction
    grid[r2][c2] &= ~OPPOSITE[direction]
    return True


"""
Set up for Kruskal's algorithm
"""


def collect_edges(grid: npt.NDArray[Any]) -> list[tuple[int, int, int]]:
    edges: list[tuple[int, int, int]] = []

    for r in range(len(grid)):

        for c in range(len(grid[0])):
            if is_modifiable(grid, r, c):
                if in_bounds(grid, r + 1, c) and is_modifiable(grid, r + 1, c):
                    edges.append((r, c, S))
                if in_bounds(grid, r, c + 1) and is_modifiable(grid, r, c + 1):
                    edges.append((r, c, E))

    return edges


"""
Set up for Prim's algorithm
"""


def get_modifiable_neighbors(grid: npt.NDArray[Any],
                             r: int, c: int) -> list[tuple[int, int, int]]:

    result: list[tuple[int, int, int]] = []

    for i in range(len(DIRECTIONS)):
        d = DIRECTIONS[i]
        dr, dc = DIR_DELTA[d]
        nr, nc = r + dr, c + dc
        if in_bounds(grid, nr, nc) and is_modifiable(grid, nr, nc):
            result.append((d, nr, nc))

    return result


def cell_index(grid: npt.NDArray[Any], r: int, c: int) -> int:
    return r * len(grid[0]) + c


"""
Union find, a list of 'structures' that will later join
"""


def make_uf(n: int) -> list[int]:
    uf: list[int] = []

    for i in range(n):
        uf.append(i)

    return uf


def find(uf: list[int], x: int) -> int:
    while uf[x] != x:
        uf[x] = uf[uf[x]]
        x = uf[x]
    return x


def union(uf: list[int], x: int, y: int) -> bool:
    rx, ry = find(uf, x), find(uf, y)
    if rx == ry:
        return False
    uf[rx] = ry
    return True


"""
Kruskal's algorithm
"""


def kruskal(grid: npt.NDArray[Any]) -> npt.NDArray[Any]:
    uf = make_uf(len(grid) * len(grid[0]))
    edges = collect_edges(grid)
    random.shuffle(edges)

    for i in range(len(edges)):
        r, c, d = edges[i]
        dr, dc = DIR_DELTA[d]
        nr, nc = r + dr, c + dc
        if union(uf, cell_index(grid, r, c), cell_index(grid, nr, nc)):
            carve(grid, r, c, nr, nc, d)

    return grid


"""
Prim's algorithm
"""


def prim(grid: npt.NDArray[Any],
         start_r: int, start_c: int) -> npt.NDArray[Any]:

    frontier: list[tuple[int, int, int, int, int]] = []

    def push_frontiers(r: int, c: int) -> None:
        neighbors = get_modifiable_neighbors(grid, r, c)

        for i in range(len(neighbors)):
            d, nr, nc = neighbors[i]
            frontier.append((r, c, d, nr, nc))

    push_frontiers(start_r, start_c)

    while frontier:
        idx = random.randrange(len(frontier))
        frontier[idx], frontier[-1] = frontier[-1], frontier[idx]
        from_r, from_c, d, to_r, to_c = frontier.pop()

        if not is_modifiable(grid, to_r, to_c):
            continue

        carve(grid, from_r, from_c, to_r, to_c, d)
        push_frontiers(to_r, to_c)

    return grid


def seal_isolated_pockets(grid: npt.NDArray[Any],
                          entry: tuple[int, int],) -> None:

    reachable: set[tuple[int, int]] = {entry}
    queue: list[tuple[int, int]] = [entry]
    qi = 0

    while qi < len(queue):
        r, c = queue[qi]
        qi += 1

        for i in range(len(DIRECTIONS)):
            d = DIRECTIONS[i]
            dr, dc = DIR_DELTA[d]
            nr, nc = r + dr, c + dc
            if (
                in_bounds(grid, nr, nc)
                and (nr, nc) not in reachable
                and grid[nr][nc] != BARRIER
            ):
                reachable.add((nr, nc))
                queue.append((nr, nc))

    for r in range(len(grid)):

        for c in range(len(grid[0])):
            if grid[r][c] != BARRIER and (r, c) not in reachable:
                grid[r][c] = BARRIER
            c += 1
        r += 1


def fill(mat: npt.NDArray[Any], entry: tuple[int, int],
         algorithm: str, seed: int = 42,) -> npt.NDArray[Any]:

    random.seed(seed)
    grid = mat
    seal_isolated_pockets(grid, entry)

    if algorithm == 'kruskal':
        return kruskal(grid)
    elif algorithm == 'prim':
        return prim(grid, entry[0], entry[1])
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
