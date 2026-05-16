import numpy as np
import numpy.typing as npt
from mazegen_pkg import MazeGenerator
import mazegen_perfect


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


def get_cell_matrix(grid: npt.NDArray, new_grid: npt.NDArray):

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


def translate_byte(intersection):

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

    return dict_char[intersection]



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
def print_final_grid(grid: npt.NDArray) -> None:

    height, width = grid.shape

    for row in range(height):
        line = ''
        for col in range(width):
            cell = grid[row][col]
            line += str(cell)
        print(line)




if __name__ == '__main__':

    SIZE  = (20, 30)
    SEED  = 42
    ENTRY = (0, 0)
    EXIT  = (2, 3)

    maze_gen = MazeGenerator(SIZE, SEED)
    mat = maze_gen.generate(ENTRY, EXIT)
    mat = maze_gen.paint_42(mat)
    mat = np.where(mat == 15, BARRIER, MODIFIABLE)

    print('Kruskal (algo1)')
    try:
        kruskal_mat = mazegen_perfect.fill(mat, ENTRY, EXIT, algorithm='algo1', seed=SEED)
    except ValueError as e:
        print(e)

    print(kruskal_mat)
    new_grid = set_edges(kruskal_mat)
    new_mat = get_cell_matrix(kruskal_mat, new_grid)

    print_final_grid(new_mat)
