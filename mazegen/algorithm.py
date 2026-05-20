import random
from .high_definitions import MODIFIABLE, BARRIER
from .high_definitions import S, E, OPPOSITE, DIR_DELTA, DIRECTIONS
import numpy.typing as npt
import numpy as np


def in_bounds(grid: npt.NDArray[np.uint8], r: int, c: int) -> bool:
    return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]


def is_modifiable(grid: npt.NDArray[np.integer], r: int, c: int) -> bool:
    return int(grid[r][c]) == MODIFIABLE


def carve(grid: npt.NDArray[np.uint8],
          r1: int, c1: int, r2: int, c2: int, direction: int,) -> bool:
    """
    Destroys a wall between cells, carving it
    """
    if grid[r1][c1] == BARRIER or grid[r2][c2] == BARRIER:
        return False

    grid[r1][c1] &= ~direction
    grid[r2][c2] &= ~OPPOSITE[direction]
    return True


def collect_edges(grid: npt.NDArray[np.uint8]) -> list[tuple[int, int, int]]:
    """
    Set up for Kruskal's algorithm
    """
    edges: list[tuple[int, int, int]] = []
    height, width = grid.shape

    for r in range(height):

        for c in range(width):
            if is_modifiable(grid, r, c):
                if in_bounds(grid, r + 1, c) and is_modifiable(grid, r + 1, c):
                    edges.append((r, c, S))
                if in_bounds(grid, r, c + 1) and is_modifiable(grid, r, c + 1):
                    edges.append((r, c, E))

    return edges


def get_modifiable_neighbors(grid: npt.NDArray[np.uint8],
                             r: int, c: int) -> list[tuple[int, int, int]]:
    """
    Set up for Prim's algorithm
    """
    result: list[tuple[int, int, int]] = []

    for dir in DIRECTIONS:
        dr, dc = DIR_DELTA[dir]
        nr, nc = r + dr, c + dc
        if in_bounds(grid, nr, nc) and is_modifiable(grid, nr, nc):
            result.append((dir, nr, nc))

    return result


def cell_index(grid: npt.NDArray[np.uint8], r: int, c: int) -> int:
    return r * len(grid[0]) + c


def make_uf(n: int) -> list[int]:
    """
    Union find, a list of 'structures' that will later join
    """
    return list(range(n))


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


def kruskal(grid: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    height, width = grid.shape
    uf = make_uf(height * width)
    edges = collect_edges(grid)
    random.shuffle(edges)

    for i in range(len(edges)):
        r, c, d = edges[i]
        dr, dc = DIR_DELTA[d]
        nr, nc = r + dr, c + dc
        if union(uf, cell_index(grid, r, c), cell_index(grid, nr, nc)):
            carve(grid, r, c, nr, nc, d)

    return grid


def prim(grid: npt.NDArray[np.uint8],
         start_r: int, start_c: int) -> npt.NDArray[np.uint8]:

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


def seal_isolated_pockets(grid: npt.NDArray[np.uint8],
                          entry: tuple[int, int],) -> None:
    """
    Implements a BFS (Breadth-First Search), a flood-fill-like algorithm.
    Starting from the given entry coordinates, it explores all reachable
    cells. Any cell that is not reachable from the entry is treated as
    isolated and is converted into a barrier.
    """
    reachable: set[tuple[int, int]] = {entry}
    queue: list[tuple[int, int]] = [entry]
    qi = 0

    while qi < len(queue):
        r, c = queue[qi]
        qi += 1

        for dir in DIRECTIONS:
            dr, dc = DIR_DELTA[dir]
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


def fill(mat: npt.NDArray[np.uint8], entry: tuple[int, int],
         algorithm: str, seed: int = 42,) -> npt.NDArray[np.uint8]:

    random.seed(seed)
    grid = mat
    seal_isolated_pockets(grid, entry)

    if algorithm == 'kruskal':
        return kruskal(grid)
    elif algorithm == 'prim':
        return prim(grid, entry[0], entry[1])
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
