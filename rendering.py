import numpy as np
import numpy.typing as npt
from mazegen_pkg import MazeGenerator
import mazegen_perfect
from rgb_text import rgb_text
import sys
import time

#it is what we get from your mazegen, F are the 42
MODIFIABLE: int = 0xF
BARRIER:    int = 0xFF #edges and 42


#   Bit 0 → N (0x1)   North wall
#   Bit 1 → E (0x2)   East  wall
#   Bit 2 → S (0x4)   South wall
#   Bit 3 → W (0x8)   West  wall

NORTH: int = 0x1
EAST: int = 0x2
SOUTH: int = 0x4
WEST: int = 0x8

WALL_BITS: list[int] = [NORTH, EAST, SOUTH, WEST]

# No basta solo con mirar la diagonal, hay que mirar la izquierda y la de arriba
def byte_intersection(cell, diagonal, left, up):

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


def set_cross(grid: npt.NDArray, new_grid: npt.NDArray):

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

            #print("Cell", cell)
            #print("Diagonal", grid[i-1][j-1])
            #print("Intersection", byte_intersection(cell, grid[i-1][j-1]))
       
    return new_grid


def translate_byte(intersection) -> str:

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


def set_entry_exit(grid: npt.NDArray, entry, exit, size):

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


def set_edges(grid: npt.NDArray):

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

            #print("Cell:", cell)
            #print("Diagonal", diagonal)
            #print("Intersection", intersection)
    
    return new_grid


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


def save_maze_to_txt(grid: npt.NDArray):

    height, width = grid.shape

    for row in range(height):
        line = ''
        for col in range(width):
            cell = grid[row][col]
            line += f'{cell:X}'  

        with open("maze.txt", "a") as maze:
            maze.write(line + '\n')

def render( anim_grid: npt.NDArray, entry: tuple[int, int], exit_coord: tuple[int, int], size: tuple[int, int],) -> None:
    rendered = set_edges(anim_grid)
    rendered = set_cross(anim_grid, rendered)
    rendered = set_entry_exit(rendered, entry, exit_coord, size)
    sys.stdout.write('\033[H\033[2J\033[3J')
    sys.stdout.flush()
    print_final_grid(rendered)


def animate_build( grid: npt.NDArray, entry: tuple[int, int], exit_coord: tuple[int, int], size: tuple[int, int], delay: float = 0.05,) -> None:

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
    render(anim_grid, entry, exit_coord, size)
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
                        render(anim_grid, entry, exit_coord, size)
                        time.sleep(delay)
                    bit_idx = bit_idx + 1
            col = col + 1
        row = row + 1

if __name__ == '__main__':

    SIZE  = (10, 15)
    SEED  = 42
    ENTRY = (1, 1)
    EXIT  = (8, 5)

	#generation
    maze_gen = MazeGenerator(SIZE, SEED)
    mat = maze_gen.generate(ENTRY, EXIT)
    mat = maze_gen.paint_42(mat)
    mat = np.where(mat == 15, BARRIER, MODIFIABLE)

    print('Kruskal (algo1)')
    try:
        kruskal_mat = mazegen_perfect.fill(mat, ENTRY, EXIT, algorithm='algo1', seed=SEED)
    except ValueError as e:
        print(e)

    animate_build(kruskal_mat, ENTRY, EXIT, SIZE, delay=0.07)

	#internal
    save_maze_to_txt(kruskal_mat)
    new_grid = set_edges(kruskal_mat)
    new_mat = set_cross(kruskal_mat, new_grid)
    new_mat = set_entry_exit(new_mat, ENTRY, EXIT, SIZE)
	#printing
    #print_final_grid(new_mat)

