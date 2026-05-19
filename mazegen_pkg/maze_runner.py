from .generator import in_bounds
from .high_definitions import OPPOSITE, DIR_DELTA, DIR_CHAR, DIRECTIONS
import numpy.typing as npt
from typing import Any
import numpy as np


def has_passage(grid: npt.NDArray[np.integer],
                row: int, col: int, direction: int) -> bool:

    return (int(grid[row][col]) & direction) == 0


def open_wall(grid: npt.NDArray[np.integer], row1: int, col1: int,
              row2: int, col2: int, direction: int) -> None:

    grid[row1][col1] &= ~direction
    grid[row2][col2] &= ~OPPOSITE[direction]


def solver(grid: npt.NDArray[Any],
           entry: tuple[int, int],
           exit_coord: tuple[int, int],) -> str | None:

    start_row, start_col = entry
    end_row, end_col = exit_coord

    if (
        not in_bounds(grid, start_row, start_col) or
        not in_bounds(grid, end_row, end_col)
    ):
        return None

    prev: dict[tuple[int, int], tuple[int, int] | None] = {entry: None}
    queue: list[tuple[int, int]] = [entry]

    while queue:
        row, col = queue.pop(0)
        if (row, col) == exit_coord:
            directions: list[str] = []
            current: tuple[int, int] = exit_coord

            while prev[current] is not None:
                parent = prev[current]
                assert parent is not None
                pr, pc = parent
                delta_row = current[0] - pr
                delta_col = current[1] - pc

                for wall_dir in DIRECTIONS:
                    if DIR_DELTA[wall_dir] == (delta_row, delta_col):
                        directions.append(DIR_CHAR[wall_dir])
                        break

                current = (pr, pc)
            directions.reverse()
            return "".join(directions)

        for wall_dir in DIRECTIONS:
            if has_passage(grid, row, col, wall_dir):
                delta_row, delta_col = DIR_DELTA[wall_dir]
                next_row, next_col = row + delta_row, col + delta_col
                if (
                    in_bounds(grid, next_row, next_col) and
                    (next_row, next_col) not in prev
                ):
                    prev[(next_row, next_col)] = (row, col)
                    queue.append((next_row, next_col))

    return None


def open_loop(
        grid: npt.NDArray[Any],
        entry: tuple[int, int],
        exit_coord: tuple[int, int]
        ) -> tuple[tuple[int, int], tuple[int, int]] | None:

    dist_entry: dict[tuple[int, int], int] = {entry: 0}
    dist_exit: dict[tuple[int, int], int] = {exit_coord: 0}
    queue_entry: list[tuple[int, int]] = [entry]
    queue_exit: list[tuple[int, int]] = [exit_coord]

    while queue_entry or queue_exit:
        if queue_entry:
            row, col = queue_entry.pop(0)

            for i in range(len(DIRECTIONS)):
                wall_dir: int = DIRECTIONS[i]
                delta_row, delta_col = DIR_DELTA[wall_dir]
                next_row, next_col = row + delta_row, col + delta_col

                if in_bounds(grid, next_row, next_col):
                    if not has_passage(grid, row, col, wall_dir):
                        if (next_row, next_col) in dist_exit:
                            open_wall(
                                grid, row, col, next_row, next_col, wall_dir)
                            return (row, col), (next_row, next_col)
                    elif (next_row, next_col) not in dist_entry:
                        dist_entry[(next_row,
                                    next_col)] = dist_entry[(row, col)] + 1
                        queue_entry.append((next_row, next_col))

        if queue_exit:
            row, col = queue_exit.pop(0)

            for i in range(len(DIRECTIONS)):
                wall_dir = DIRECTIONS[i]
                delta_row, delta_col = DIR_DELTA[wall_dir]
                next_row, next_col = row + delta_row, col + delta_col
                if in_bounds(grid, next_row, next_col):
                    if not has_passage(grid, row, col, wall_dir):
                        if (next_row, next_col) in dist_entry:
                            open_wall(
                                grid, row, col, next_row, next_col, wall_dir)
                            return (row, col), (next_row, next_col)
                    elif (next_row, next_col) not in dist_exit:
                        dist_exit[(next_row,
                                   next_col)] = dist_exit[(row, col)] + 1
                        queue_exit.append((next_row, next_col))

    return None


def make_imperfect(grid: npt.NDArray[Any],
                   entry: tuple[int, int],
                   exit_coord: tuple[int, int],) -> str:

    open_loop(grid, entry, exit_coord)
    solution = solver(grid, entry, exit_coord)
    return solution
