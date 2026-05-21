from __future__ import annotations
import sys
import numpy as np
import numpy.typing as npt
from typing import Any
from .parsing import open_file, get_keys_dict
from .parsing import check_data_format, check_entry_exit
from .algorithm import fill
from .rgb_text import get_rgb_value
from .maze_runner import make_imperfect, solver
from .high_definitions import MODIFIABLE, BARRIER
from .renderer import render
from .animations import animate_build, animate_solution


class MazeGenerator():
    def __init__(self) -> None:

        keys_dict = self.check_parameters()

        if bool(keys_dict):
            self.size: tuple[int,
                             int] = keys_dict['HEIGHT'], keys_dict['WIDTH']
            self.seed: int = keys_dict['SEED']
            self.entry: tuple[int, int] = keys_dict['ENTRY']
            self.exit_coord: tuple[int, int] = keys_dict['EXIT']
            self.algo: str = keys_dict['ALGORITHM'].lower()
            self.perfect: bool = keys_dict['PERFECT']
            self.output: str = keys_dict['OUTPUT_FILE']
            self.colours = self.MazeColours

    def generate_base(self) -> npt.NDArray[np.uint8]:
        np.random.seed(self.seed)
        zeros_mat = np.zeros(self.size, dtype=int)
        self.paint_42(zeros_mat)
        mat = np.where(zeros_mat == 15, BARRIER, MODIFIABLE)

        return mat

    def generate_maze(self) -> npt.NDArray[np.uint8]:

        keys_dict = self.check_parameters()

        base = self.generate_base()

        if not check_entry_exit(keys_dict, base):
            print("Impossible maze parameters")
            exit()

        try:
            maze = fill(base, self.entry, algorithm=self.algo, seed=self.seed)
        except ValueError as e:
            print(e)

        if not self.perfect:
            make_imperfect(maze, self.entry, self.exit_coord)

        return maze

    def check_parameters(self) -> dict[str, Any]:
        args = sys.argv[1:]

        if len(args) != 1:
            print("Incorrect number of arguments provided")
            exit()

        config_file = sys.argv[1]
        config = open_file(config_file)

        if not config:
            print("Config file is empty")
            exit()

        keys_dict = get_keys_dict(config)

        if not bool(keys_dict):
            print("Missing or invalid parameters in config file")
            exit()
        try:
            keys_dict = check_data_format(keys_dict)
        except Exception as e:
            print(e)
            exit()

        return keys_dict

    def paint_42(self, mat: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:

        if self.size[0] > 5 and self.size[1] > 7:

            n_blocks = max(min(int(self.size[0]/(3 * 2)),
                               int(self.size[1]/(3 * 2))), 3)
            space = 1
            n_width = n_blocks * 2 + space
            n_height = n_width - 2

            x = int(self.size[1]/2 - n_height/2) - 1
            if (self.size[0] <= 6 and self.size[1] <= 8):
                y = int(self.size[0]/2 - n_width/2)
            else:
                y = int(self.size[0]/2 - n_width/2) + 1

            for i in range(0, n_blocks):
                mat[y + i][x] = 15
                mat[y + n_blocks - 1][x + i] = 15
                mat[y + n_blocks + i - 1][x + n_blocks - 1] = 15

            for j in range(0, n_blocks):
                mat[y][x + n_blocks + j + space] = 15
                mat[y + j][x + 2 * n_blocks + space - 1] = 15
                mat[y + n_blocks - 1][x + n_blocks + space + j] = 15
                mat[y + n_blocks + j - 1][x + n_blocks + space] = 15
                mat[y + 2 * n_blocks - 2][x + n_blocks + space + j] = 15

        return mat

    def maze_renderer(self, maze: npt.NDArray[np.uint8],
                      colours: MazeColours) -> None:
        render(maze, self.entry, self.exit_coord, self.size, colours)

    def maze_animate(self, maze: npt.NDArray[np.uint8],
                     colours: MazeColours) -> None:
        animate_build(
            maze, self.entry, self.exit_coord, self.size, colours, 0.02)

    def maze_solve(self, maze: npt.NDArray[np.uint8],
                   colours: MazeColours) -> None:
        solution = solver(maze, self.entry, self.exit_coord)
        animate_solution(
            maze,
            self.entry, self.exit_coord, self.size,
            solution, colours, 0.02)

    class MazeColours:
        def __init__(self,
                     wall_r: int = 255, wall_g: int = 255, wall_b: int = 255,
                     barrier_r: int = 128,
                     barrier_g: int = 128,
                     barrier_b: int = 128,) -> None:

            self.wall_r = wall_r
            self.wall_g = wall_g
            self.wall_b = wall_b
            self.barrier_r = barrier_r
            self.barrier_g = barrier_g
            self.barrier_b = barrier_b

        def ask_colours(self) -> None:
            print("Wall colour:")
            self.wall_r = get_rgb_value("red")
            self.wall_g = get_rgb_value("green")
            self.wall_b = get_rgb_value("blue")
            print("Barrier colour:")
            self.barrier_r = get_rgb_value("red")
            self.barrier_g = get_rgb_value("green")
            self.barrier_b = get_rgb_value("blue")
