#!/usr/bin/env python3

from mazegen_pkg import MazeGenerator
from typing import Any
import sys
import numpy as np
import numpy.typing as npt
import mazegen_perfect
from rendering import save_maze_to_txt, set_cross, set_edges, set_entry_exit, animate_build, animate_solution, MazeColours, ask_colours
from maze_runner import solver


#it is what we get from your mazegen, F are the 42
MODIFIABLE: int = 0xF
BARRIER:    int = 0xFF #edges and 42

def open_file(config_file) -> list[str]:
    config: list[str] = []
    try:
        with open(config_file) as config_file:
            config: list[str] = config_file.readlines()
    except Exception as e:
        print(f"File not found: {e}")

    return config


def check_keys(config) -> bool:

    keys: list[str] = []
    allowed_keys = [
        'WIDTH', 
        'HEIGHT', 
        'ENTRY', 
        'EXIT', 
        'OUTPUT_FILE', 
        'PERFECT', 
        'SEED', 
        'ALGORITHM'
    ]

    for line in config:
        line.strip()
        if not line.startswith('#'):
            key: str = line.split('=')[0].strip()
            keys.append(key.upper())
    
    return sorted(allowed_keys) == sorted(keys)


def get_keys_dict(config) -> dict[str, Any]:
    keys_dict = {}

    if check_keys(config):    
        for item in config:
            try:
                key, value = item.strip().split('=', 1)
                key = key.upper()
                keys_dict[key] = value

            except Exception as e:
                print(e)

    return keys_dict


def parse_coordinate(s: str) -> tuple[int, int] | None:
    parts = s.split(',')

    if len(parts) != 2:
        return None
    
    if parts[0].isdigit() and parts[1].isdigit():
        return int(parts[0]), int(parts[1]) 
    
    return None


def check_data_format(keys_dict):

    algo_list: list[str] = ['algo1']
    for item in keys_dict:

        if item in ('WIDTH', 'HEIGHT', 'SEED'):
            keys_dict[item] = int(keys_dict[item])

        elif item == 'PERFECT':
            if keys_dict[item].upper() == 'TRUE':
                keys_dict[item] = True
            elif keys_dict[item].upper() == 'FALSE':
                keys_dict[item] = False
            else:
                raise Exception("The value of Perfect parameter is not a boolean")

        elif item in ('ENTRY', 'EXIT'):
            coord = parse_coordinate(keys_dict[item])
            if coord is not None:
                keys_dict[item] = coord
            else:
                raise Exception("Wrong coordinates")
            
        elif item == 'ALGORITHM':
            if keys_dict[item] not in algo_list:
                raise Exception("Unknown algorithm")
 
    return(keys_dict)


def check_entry_exit(keys_dict, mat):
    entry = keys_dict['ENTRY']
    exit_coord = keys_dict['EXIT']
    width = keys_dict['WIDTH']
    height = keys_dict['HEIGHT']

    if entry == exit_coord:
        return False
    
    if (
        entry[0] >= height or
        exit_coord[0] >= height or
        entry[1] >= width or
        exit_coord[1] >= width
    ):
        return False
    
    if (
        mat[entry[0]][entry[1]] == BARRIER or
        mat[exit_coord[0]][exit_coord[1]] == BARRIER
    ):
        return False

    return True


#just for testing
def print_final_grid(grid: list[list[str]]) -> None:

    height = len(grid)#this should come from the config directly later
    width = len(grid[0])

    for row in range(height):
        line = ''
        for col in range(width):
            cell = grid[row][col]
            line += str(cell)
        print(line)


def animate_from_config(config_file: str, colours: MazeColours) -> None:
    config = open_file(config_file)
    if not config:
        return

    keys_dict = get_keys_dict(config)
    if not bool(keys_dict):
        print("Invalid format")
        return

    try:
        keys_dict = check_data_format(keys_dict)
    except Exception as e:
        print(e)
        return

    size       = keys_dict['HEIGHT'], keys_dict['WIDTH']
    seed       = keys_dict['SEED']
    entry      = keys_dict['ENTRY']
    exit_coord = keys_dict['EXIT']

    maze_gen = MazeGenerator(size, seed)
    mat = maze_gen.generate(entry, exit_coord)
    mat = maze_gen.paint_42(mat)
    mat = np.where(mat == 15, BARRIER, MODIFIABLE)

    if not check_entry_exit(keys_dict, mat):
        print("Impossible maze parameters")
        return

    try:
        kruskal_mat = mazegen_perfect.fill(mat, entry, exit_coord, algorithm=keys_dict['ALGORITHM'], seed=seed)
    except ValueError as e:
        print(e)
        return

    animate_build(kruskal_mat, entry, exit_coord, size, colours=colours)

    solution = solver(kruskal_mat.tolist(), entry, exit_coord)
    if solution:
        animate_solution(kruskal_mat, entry, exit_coord, size, solution, colours=colours)


def _setup_maze(
    config_file: str,
) -> tuple[npt.NDArray, tuple[int, int], tuple[int, int], tuple[int, int]] | None:
    config = open_file(config_file)
    if not config:
        return None

    keys_dict = get_keys_dict(config)
    if not bool(keys_dict):
        print("Invalid format")
        return None

    try:
        keys_dict = check_data_format(keys_dict)
    except Exception as e:
        print(e)
        return None

    size       = keys_dict['HEIGHT'], keys_dict['WIDTH']
    seed       = keys_dict['SEED']
    entry      = keys_dict['ENTRY']
    exit_coord = keys_dict['EXIT']

    maze_gen = MazeGenerator(size, seed)
    mat = maze_gen.generate(entry, exit_coord)
    mat = maze_gen.paint_42(mat)
    mat = np.where(mat == 15, BARRIER, MODIFIABLE)

    if not check_entry_exit(keys_dict, mat):
        print("Impossible maze parameters")
        return None

    try:
        kruskal_mat = mazegen_perfect.fill(mat, entry, exit_coord, algorithm=keys_dict['ALGORITHM'], seed=seed)
    except ValueError as e:
        print(e)
        return None

    return kruskal_mat, entry, exit_coord, size


def play_build(config_file: str, colours: MazeColours) -> None:
    result = _setup_maze(config_file)
    if result is None:
        return
    kruskal_mat, entry, exit_coord, size = result
    animate_build(kruskal_mat, entry, exit_coord, size, colours=colours)


def play_solve(config_file: str, colours: MazeColours) -> None:
    result = _setup_maze(config_file)
    if result is None:
        return
    kruskal_mat, entry, exit_coord, size = result
    solution = solver(kruskal_mat.tolist(), entry, exit_coord)
    if solution:
        animate_solution(kruskal_mat, entry, exit_coord, size, solution, colours=colours)


def if_main() -> None:

    args = sys.argv[1:]
    if len(args) != 1:
        print("Incorrect number of arguments provided")
        exit()

    config_file = sys.argv[1]
    config = open_file(config_file) 

    if not config:
        exit()
           
    keys_dict = get_keys_dict(config)

    if not bool(keys_dict):
        print("Invalid format")
        exit()
    try:
        keys_dict = check_data_format(keys_dict)
    except Exception as e:
        print(e)
        exit()

    size = keys_dict['HEIGHT'], keys_dict['WIDTH']
    seed = keys_dict['SEED']
    entry = keys_dict['ENTRY']
    exit_coord = keys_dict['EXIT']

    maze_gen = MazeGenerator(size, seed)
    mat = maze_gen.generate(entry, exit_coord)
    mat = maze_gen.paint_42(mat)
    mat = np.where(mat == 15, BARRIER, MODIFIABLE)

    if not check_entry_exit(keys_dict, mat):
        print("Impossible maze parameters")
        exit()

    print('Kruskal (algo1)')
    try:
        kruskal_mat = mazegen_perfect.fill(mat, entry, exit_coord, algorithm='algo1', seed=seed)
    except ValueError as e:
        print(e)

    save_maze_to_txt(kruskal_mat)
    new_grid = set_edges(kruskal_mat)
    new_mat = set_cross(kruskal_mat, new_grid)
    new_mat = set_entry_exit(new_mat, entry, exit_coord, size)

    print_final_grid(new_mat)



if __name__ == "__main__":
    colours = MazeColours()
    ask_colours(colours)
    play_build('config.txt', colours)
    play_solve('config.txt', colours)
    ask_colours(colours)
    play_build('config.txt', colours)
    play_solve('config.txt', colours)
