from .high_definitions import MODIFIABLE, BARRIER, CHAR_DELTA, SOLUTION_COLOUR, WALL_BITS
import sys
import time
import numpy.typing as npt
import numpy as np
from .renderer import render, set_cross, set_edges, set_entry_exit, colourise_grid, print_final_grid


def animate_solution(grid: npt.NDArray, entry: tuple[int, int], exit_coord: tuple[int, int], size: tuple[int, int], solution: str, delay: float = 0.05, colours = None,) -> None:
    rendered = set_edges(grid)
    rendered = set_cross(grid, rendered)
    rendered = set_entry_exit(rendered, entry, exit_coord, size)
    if colours is not None:
        rendered = colourise_grid(rendered, colours)
    row, col = entry
    idx: int = 0
    while idx < len(solution):
        delta_row, delta_col = CHAR_DELTA[solution[idx]]
        row += delta_row
        col += delta_col
        if (row, col) != exit_coord:
            rendered[row * 2 + 1][col * 2 + 1] = SOLUTION_COLOUR
        sys.stdout.write('\033[H\033[2J\033[3J')
        sys.stdout.flush()
        print_final_grid(rendered)
        time.sleep(delay)
        idx += 1


def animate_build(grid: npt.NDArray, entry: tuple[int, int], exit_coord: tuple[int, int], size: tuple[int, int], delay: float = 0.05, colours = None,) -> None:

    height, width = grid.shape
    anim_grid = np.full((height, width), MODIFIABLE, dtype=int)

    row: int = 0
    while row < height:
        col: int = 0
        while col < width:
            if grid[row][col] == BARRIER:
                anim_grid[row][col] = BARRIER
            col = col + 1
        row = row + 1
    render(anim_grid, entry, exit_coord, size, colours)
    time.sleep(delay)
    row = 0
    while row < height:
        col = 0
        while col < width:
            target = int(grid[row][col])
            if target != BARRIER:
                bit_idx: int = 0
                while bit_idx < len(WALL_BITS):
                    wall_bit = WALL_BITS[bit_idx]
                    if not (target & wall_bit) and (anim_grid[row][col] & wall_bit):
                        anim_grid[row][col] &= ~wall_bit
                        render(anim_grid, entry, exit_coord, size, colours)
                        time.sleep(delay)
                    bit_idx = bit_idx + 1
            col = col + 1
        row = row + 1
