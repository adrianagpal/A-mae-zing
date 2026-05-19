from __future__ import annotations
from .high_definitions import MODIFIABLE, BARRIER
from .high_definitions import CHAR_DELTA, SOLUTION_COLOUR, WALL_BITS
from .renderer import render, set_cross, set_edges, set_entry_exit
from .renderer import colourise_grid, print_final_grid
import sys
import time
import numpy.typing as npt
import numpy as np
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from .mazegen import MazeGenerator


def animate_solution(grid: npt.NDArray[Any],
                     entry: tuple[int, int],
                     exit_coord: tuple[int, int],
                     size: tuple[int, int],
                     solution: str,
                     colours: MazeGenerator.MazeColours | None = None,
                     delay: float = 0.05) -> None:

    rendered = set_edges(grid)
    rendered = set_cross(grid, rendered)
    rendered = set_entry_exit(rendered, entry, exit_coord, size)

    if colours is not None:
        rendered = colourise_grid(rendered, colours)
    row, col = entry

    for idx in range(len(solution)):
        delta_row, delta_col = CHAR_DELTA[solution[idx]]
        row += delta_row
        col += delta_col

        if (row, col) != exit_coord:
            rendered[row * 2 + 1][col * 2 + 1] = SOLUTION_COLOUR

        sys.stdout.write('\033[H\033[2J\033[3J')
        sys.stdout.flush()
        print_final_grid(rendered)
        time.sleep(delay)


def animate_build(grid: npt.NDArray[Any],
                  entry: tuple[int, int],
                  exit_coord: tuple[int, int],
                  size: tuple[int, int],
                  colours: MazeGenerator.MazeColours,
                  delay: float = 0.05) -> None:

    height, width = grid.shape
    anim_grid = np.full((height, width), MODIFIABLE, dtype=int)

    for row in range(height):

        for col in range(width):
            if grid[row][col] == BARRIER:
                anim_grid[row][col] = BARRIER

    render(anim_grid, entry, exit_coord, size, colours)
    time.sleep(delay)

    for row in range(height):

        for col in range(width):
            target = int(grid[row][col])

            if target != BARRIER:
                current = anim_grid[row][col]

                for wall_bit in WALL_BITS:
                    if not (target & wall_bit) and (current & wall_bit):
                        anim_grid[row][col] &= ~wall_bit
                        render(anim_grid, entry, exit_coord, size, colours)
                        time.sleep(delay)
