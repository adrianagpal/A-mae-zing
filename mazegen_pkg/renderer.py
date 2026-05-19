from __future__ import annotations
import numpy as np
import numpy.typing as npt
import random
import sys
from .high_definitions import WALL_CHARS, NORTH, SOUTH, EAST, WEST
from .rgb_text import rgb_text
from .maze_runner import solver
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from .mazegen import MazeGenerator


def colourise_grid(grid: npt.NDArray[np.str_],
                   colours: MazeGenerator.MazeColours) -> npt.NDArray[np.str_]:

    for row_idx in range(len(grid)):

        for col_idx in range(len(grid[row_idx])):
            cell = grid[row_idx][col_idx]
            if cell in WALL_CHARS:
                grid[row_idx][col_idx] = rgb_text(cell,
                                                  colours.wall_r,
                                                  colours.wall_g,
                                                  colours.wall_b)
            elif cell == '█':
                grid[row_idx][col_idx] = rgb_text(cell,
                                                  colours.barrier_r,
                                                  colours.barrier_g,
                                                  colours.barrier_b)
    return grid


"""
To find the character to return, we have to look the cell itself,
the diagonal up left, the cell to the left, and the cell up.
"""


def byte_intersection(cell: int, diagonal: int, left: int, up: int) -> int:

    byte = 0

    east = cell & NORTH
    south = cell & WEST
    north = diagonal & EAST
    west = diagonal & SOUTH
    west_left = left & NORTH
    south_left = left & EAST
    north_up = up & WEST
    east_up = up & SOUTH

    if east or east_up:
        byte = byte | EAST
    if west or west_left:
        byte = byte | WEST
    if north or north_up:
        byte = byte | NORTH
    if south or south_left:
        byte = byte | SOUTH

    return byte


def set_cross(grid: npt.NDArray[Any],
              new_grid: npt.NDArray[Any]) -> npt.NDArray[Any]:

    height, width = grid.shape

    for i in range(height):

        for j in range(width):

            cell = grid[i][j]
            idx_row = i * 2 + 1
            idx_col = j * 2 + 1

            if cell & NORTH:
                new_grid[idx_row - 1][idx_col] = '═'
            if cell & EAST:
                new_grid[idx_row][idx_col + 1] = '║'
            if cell & WEST:
                new_grid[idx_row][idx_col - 1] = '║'
            if cell & SOUTH:
                new_grid[idx_row + 1][idx_col] = '═'

            if cell == 255:
                new_grid[idx_row][idx_col] = '█'

    return new_grid


def translate_byte(intersection: int) -> str:

    dict_char = {
        0: ' ',
        NORTH: '║',
        SOUTH: '║',
        EAST: '═',
        WEST: '═',

        NORTH | SOUTH: '║',
        EAST | WEST: '═',

        NORTH | EAST: '╚',
        NORTH | WEST: '╝',
        SOUTH | EAST: '╔',
        SOUTH | WEST: '╗',

        NORTH | SOUTH | EAST: '╠',
        NORTH | SOUTH | WEST: '╣',
        EAST | WEST | NORTH: '╩',
        EAST | WEST | SOUTH: '╦',

        NORTH | SOUTH | EAST | WEST: '╬',
    }

    try:
        return dict_char[intersection]
    except KeyError:
        return dict_char[0]


def set_entry_exit(grid: npt.NDArray[Any],
                   entry: tuple[int, int],
                   exit: tuple[int, int],
                   size: tuple[int, int]) -> list[list[str]]:

    rows = size[0] * 2 + 1
    cols = size[1] * 2 + 1

    coord1_entry, coord2_entry = entry[0] * 2 + 1, entry[1] * 2 + 1
    coord1_exit, coord2_exit = exit[0] * 2 + 1, exit[1] * 2 + 1

    new_grid: list[list[str]] = []

    for idx_row in range(rows):
        row: list[str] = []
        for idx_col in range(cols):
            row.append(grid[idx_row][idx_col])
        new_grid.append(row)

    new_grid[coord1_entry][coord2_entry] = rgb_text('█', 255, 0, 0)
    new_grid[coord1_exit][coord2_exit] = rgb_text('█', 0, 255, 0)
    return new_grid


def set_edges(grid: npt.NDArray[Any]) -> npt.NDArray[np.str_]:

    height, width = grid.shape
    new_grid = np.full((2 * height + 1, 2 * width + 1), ' ', dtype=str)
    pad_grid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)

    for i in range(1, height + 2):

        for j in range(1, width + 2):

            cell = pad_grid[i][j]
            diagonal = pad_grid[i-1][j-1]
            left = pad_grid[i][j-1]
            up = pad_grid[i-1][j]

            idx_row = (i - 1) * 2 + 1
            idx_col = (j - 1) * 2 + 1

            intersection = byte_intersection(cell, diagonal, left, up)

            new_grid[idx_row - 1][idx_col - 1] = translate_byte(intersection)

    return new_grid


def save_maze_to_txt(grid: npt.NDArray[Any],
                     entry: tuple[int, int],
                     exit_coord: tuple[int, int], filename: str) -> None:

    height, width = grid.shape
    content: str = ""

    for row in range(height):
        line = ''
        for col in range(width):
            cell = 'F' if grid[row][col] == 0xFF else f'{grid[row][col]:X}'
            line += cell

        content += line + '\n'

    with open(filename, "w") as maze:
        maze.write(content)
        maze.write('\n')
        maze.write(",".join([str(entry[0]), str(entry[1])]))
        maze.write('\n')
        maze.write(",".join([str(exit_coord[0]), str(exit_coord[1])]))
        maze.write('\n')
        maze.write(solver(grid, entry, exit_coord))
        maze.write('\n')


def _build_ber_grid(grid: npt.NDArray[Any],
                    entry: tuple[int, int],
                    exit_coord: tuple[int, int],
                    c_chance: float = 0.05,) -> list[list[str]]:

    rendered = set_edges(grid)
    rendered = set_cross(grid, rendered)

    rows, cols = rendered.shape
    simple: list[list[str]] = []
    floor_positions: list[tuple[int, int]] = []

    entry_cell = (entry[0] * 2 + 1, entry[1] * 2 + 1)
    exit_cell = (exit_coord[0] * 2 + 1, exit_coord[1] * 2 + 1)

    for row_idx in range(rows):
        row: list[str] = []

        for col_idx in range(cols):
            cell = str(rendered[row_idx][col_idx])
            if cell in WALL_CHARS or cell == '█':
                row.append('1')
            else:
                row.append('0')
                if (row_idx, col_idx) not in (entry_cell, exit_cell):
                    floor_positions.append((row_idx, col_idx))
        simple.append(row)

    simple[entry_cell[0]][entry_cell[1]] = 'P'
    simple[exit_cell[0]][exit_cell[1]] = 'E'

    c_positions: list[tuple[int, int]] = []

    for idx in range(len(floor_positions)):
        if random.random() < c_chance:
            c_positions.append(floor_positions[idx])

    if not c_positions:
        c_positions.append(random.choice(floor_positions))

    for idx in range(len(c_positions)):
        row_idx, col_idx = c_positions[idx]
        simple[row_idx][col_idx] = 'C'

    return simple


def save_ber(grid: npt.NDArray[Any],
             entry: tuple[int, int],
             exit_coord: tuple[int, int],
             filename: str, c_chance: float = 0.05,) -> None:

    simple = _build_ber_grid(grid, entry, exit_coord, c_chance)
    with open(filename, 'w') as ber_file:
        for row_idx in range(len(simple)):
            ber_file.write(''.join(simple[row_idx]) + '\n')


def print_final_grid(grid: npt.NDArray[Any]) -> None:

    height = len(grid)
    width = len(grid[0])

    for row in range(height):
        line = ''
        for col in range(width):
            cell = grid[row][col]
            line += str(cell)
        print(line)


def render(anim_grid: npt.NDArray[np.integer],
           entry: tuple[int, int],
           exit_coord: tuple[int, int],
           size: tuple[int, int],
           colours: MazeGenerator.MazeColours) -> None:

    rendered = set_edges(anim_grid)
    rendered = set_cross(anim_grid, rendered)
    rendered = set_entry_exit(rendered, entry, exit_coord, size)

    if colours is not None:
        rendered = colourise_grid(rendered, colours)

    sys.stdout.write('\033[H\033[2J\033[3J')
    sys.stdout.flush()
    print_final_grid(rendered)
