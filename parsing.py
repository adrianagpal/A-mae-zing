#!/usr/bin/env python3

from mazegen_pkg import MazeGenerator
from typing import Any
import sys


def open_file(config_file) -> list[str]:
    config: list[str] = []
    try:
        with open(config_file) as config_file:
            config: list[str] = config_file.readlines()
    except Exception as e:
        print(f"File not found: {e}")

    return config


"""
Checks if all required keys are provided in the config file
and there are no duplicates, or extra keys
"""
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

    print(keys_dict)
    return keys_dict


"""
Check valid coordinates without spaces
"""
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
            print(keys_dict[item].upper())
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

    print("Dictionary succesfully registered")  
    return(keys_dict)


def check_entry_exit(keys_dict):
    entry = keys_dict['ENTRY']
    exit_coord = keys_dict['EXIT']
    width = keys_dict['WIDTH']
    height = keys_dict['HEIGHT']

    if entry == exit_coord:
        return False

    if (
        entry[0] > width or
        exit_coord[0] > width or
        entry[1] > height or
        exit_coord[1] > height
    ):
        return False

    return True


def main() -> None:

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
        print(keys_dict)
    except Exception as e:
        print(e)

    if not check_entry_exit(keys_dict):
        print("Impossible maze parameters")
        exit()

    size = keys_dict['HEIGHT'], keys_dict['WIDTH']
    seed = keys_dict['SEED']
    entry = keys_dict['ENTRY']
    exit_coord = keys_dict['EXIT']

    maze_gen = MazeGenerator(size, seed)
    mat = maze_gen.generate(entry, exit_coord)
    print(maze_gen.paint_42(mat))


#def convert_to_byte():

def debug_nibble():
    x = 14
    new_nibble = swap_nibbles(x)

    print(new_nibble)
    print(new_nibble >> 0 & 1)
    print(new_nibble >> 1 & 1)
    print(new_nibble >> 2 & 1)
    print(new_nibble >> 3 & 1)

if __name__ == "__main__":
    main()

# Put random hex numbers taking into account the restrictions of the corresponding bit.
