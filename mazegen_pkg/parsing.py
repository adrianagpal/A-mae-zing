#!/usr/bin/env python3

from typing import Any
from .high_definitions import BARRIER


def open_file(config_file: str) -> list[str]:
    config: list[str] = []
    try:
        with open(config_file) as config_file:
            config = config_file.readlines()
    except Exception as e:
        print(f"File not found: {e}")

    return config


def check_keys(config: list[str]) -> bool:

    keys: list[str] = []
    allowed_keys: list[str] = [
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


def get_keys_dict(config: list[str]) -> dict[str, Any]:
    keys_dict: dict[str, Any] = {}

    if check_keys(config):    
        for item in config:
            try:
                key, value = item.strip().split('=', 1)
                key = key.upper()
                keys_dict[key] = value

            except Exception as e:
                print(e)

    return keys_dict


def parse_coordinate(coord: str) -> tuple[int, int] | None:
    parts: list[str] = coord.split(',')

    if len(parts) != 2:
        return None
    
    if parts[0].isdigit() and parts[1].isdigit():
        return int(parts[0]), int(parts[1]) 
    
    return None


def check_data_format(keys_dict: dict[str, Any]) -> dict[str, Any]:

    algo_list: list[str] = ['kruskal', 'prim']
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
            if keys_dict[item].lower() not in algo_list:
                raise Exception("Unknown algorithm")
 
    return(keys_dict)


def check_entry_exit(keys_dict, mat) -> bool:
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
