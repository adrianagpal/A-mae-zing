import random
from .high_definitions import MODIFIABLE, BARRIER, N, S, E, W, OPPOSITE, DIR_DELTA, DIRECTIONS


def in_bounds(grid: list[list[int]], r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def is_modifiable(grid: list[list[int]], r: int, c: int) -> bool:
    return grid[r][c] == MODIFIABLE


#destroys a wall between cells, carving it
def carve(grid: list[list[int]], r1: int, c1: int, r2: int, c2: int, direction: int,) -> bool:
    if grid[r1][c1] == BARRIER or grid[r2][c2] == BARRIER:
        return False
    grid[r1][c1] &= ~direction
    grid[r2][c2] &= ~OPPOSITE[direction]
    return True


#set up for kruskal
def collect_edges(grid: list[list[int]]) -> list[tuple[int, int, int]]:
    edges: list[tuple[int, int, int]] = []
    r = 0
    while r < len(grid):
        c = 0
        while c < len(grid[0]):
            if is_modifiable(grid, r, c):
                if in_bounds(grid, r + 1, c) and is_modifiable(grid, r + 1, c):
                    edges.append((r, c, S))
                if in_bounds(grid, r, c + 1) and is_modifiable(grid, r, c + 1):
                    edges.append((r, c, E))
            c = c + 1
        r = r + 1
    return edges


#set up for prim
def get_modifiable_neighbors(
    grid: list[list[int]], r: int, c: int
) -> list[tuple[int, int, int]]:
    result: list[tuple[int, int, int]] = []
    i = 0
    while i < len(DIRECTIONS):
        d = DIRECTIONS[i]
        dr, dc = DIR_DELTA[d]
        nr, nc = r + dr, c + dc
        if in_bounds(grid, nr, nc) and is_modifiable(grid, nr, nc):
            result.append((d, nr, nc))
        i = i + 1
    return result


def cell_index(grid: list[list[int]], r: int, c: int) -> int:
    return r * len(grid[0]) + c


#union find, a list of 'structures' that will later join
def make_uf(n: int) -> list[int]:
    uf: list[int] = []
    i = 0
    while i < n:
        uf.append(i)
        i += 1
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


# Algo1: Kruskal's
def kruskal(grid: list[list[int]]) -> list[list[int]]:
    uf = make_uf(len(grid) * len(grid[0]))
    edges = collect_edges(grid)
    random.shuffle(edges)

    i = 0
    while i < len(edges):
        r, c, d = edges[i]
        dr, dc = DIR_DELTA[d]
        nr, nc = r + dr, c + dc
        if union(uf, cell_index(grid, r, c), cell_index(grid, nr, nc)):
            carve(grid, r, c, nr, nc, d)
        i += 1

    return grid


# Algo2: Prim's
def prim(grid: list[list[int]], start_r: int, start_c: int) -> list[list[int]]:
    frontier: list[tuple[int, int, int, int, int]] = []

    def push_frontiers(r: int, c: int) -> None:
        neighbors = get_modifiable_neighbors(grid, r, c)
        i = 0
        while i < len(neighbors):
            d, nr, nc = neighbors[i]
            frontier.append((r, c, d, nr, nc))
            i += 1

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


def seal_isolated_pockets(grid: list[list[int]],entry: tuple[int, int],) -> None:
    reachable: set[tuple[int, int]] = {entry}
    queue: list[tuple[int, int]] = [entry]
    qi = 0
    while qi < len(queue):
        r, c = queue[qi]
        qi += 1
        i = 0
        while i < len(DIRECTIONS):
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
            i += 1

    r = 0
    while r < len(grid):
        c = 0
        while c < len(grid[0]):
            if grid[r][c] != BARRIER and (r, c) not in reachable:
                grid[r][c] = BARRIER
            c += 1
        r += 1


def fill(mat, entry: tuple[int, int], algorithm: str, seed: int = 42,) -> list[list[int]]:
    random.seed(seed)
    grid = mat
    seal_isolated_pockets(grid, entry)

    if algorithm == 'kruskal': #this will aslo come from the config
        return kruskal(grid)
    elif algorithm == 'prim':
        return prim(grid, entry[0], entry[1])
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")