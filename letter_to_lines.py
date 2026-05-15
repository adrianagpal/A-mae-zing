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

N: int = 0x1
E: int = 0x2
S: int = 0x4
W: int = 0x8

def swap_nibbles(x):
    bit_swap = x << 2
    print(bit_swap)
    first = (bit_swap >> 4) & 0xF
    print(first)
    result = bit_swap | first
    print(result)
    """Get 4 low order bits from a byte."""
    final = result & 0x0F
    return (final)

def debug_nibble():
    x = 13
    new_nibble = swap_nibbles(x)

    print(new_nibble)
    print(x >> 0 & 1)
    print(x >> 1 & 1)
    print(x >> 2 & 1)
    print(x >> 3 & 1)


# '╔' -> 9556 -> \u2554
# '╗' -> 9559 -> \u2557
# '╚' -> 9562 -> \u255A
# '╝' -> 9565 -> \u255D
# '═' -> 9552 -> \u2550
# '║' -> 9553 -> \u2551


def get_cell_matrix(grid: npt.NDArray):

    height, width = grid.shape
    new_grid = np.empty((height, width), dtype=object)
    line= []

    for i in range(height):

        for j in range(width):

            cell = np.full((3,5), ' ', dtype=str)
            val = int(grid[i][j])

            if val == 255:
                cell[1,1] = '█'
                new_grid[i][j] = cell
                continue

            if (val >> 3) & 1:
                cell[:, 0] = chr(9553)
            if (val >> 2) & 1:
                cell[2, :] = chr(9552)
            if (val >> 1) & 1:
                cell[:, 2] = chr(9553)
            if (val >> 0) & 1:
                cell[0, :] = chr(9552)

            # West and North
            if (val >> 3) & 1 and (val >> 0) & 1:

                if i != 0 and j != 0 and (grid[i-1][j] >> 3 & 1) and (grid[i][j-1] >> 0 & 1):
                    cell[0][0] = 'A'             
                
                elif i != 0 and (grid[i-1][j] >> 3 & 1):
                    cell[0][0] = '╠'
                
                elif j != 0 and (grid[i][j-1] >> 0 & 1):
                    cell[0][0] = '╦'
                
                else:
                    cell[0][0] = chr(9556) 

            # West and South
            if (val >> 3) & 1 and (val >> 2) & 1 and i != (height - 1):

                if (grid[i+1][j] >> 3 & 1):
                    cell[2][0] = '╠'
                else:
                    cell[2][0] = chr(9562) 

            # North and East
            if (val >> 0) & 1 and (val >> 1) & 1 and i != 0:

                if (grid[i-1][j] >> 1 & 1):
                    cell[0][2] = '╣'
                else:
                    cell[0][2] = chr(9559)

            # South and East
            if (val >> 2) & 1 and (val >> 1) & 1 and i != (height - 1):

                if (grid[i+1][j] >> 1 & 1):
                    cell[2][2] = '╣'
                else:
                    cell[2][2] = chr(9559)

            # West and North, with North to the side
            if (val >> 3) & 1 and (val >> 0) & 1 and j != 0:

                if (grid[i][j-1] >> 0 & 1):
                    cell[0][0] = '╦'
                else:
                    cell[0][0] = chr(9559)

            if (val >> 1) & 1 and (val >> 0) & 1 and j != (width - 1):

                if (grid[i][j+1] >> 0 & 1):
                    cell[0][2] = '╦'
                else:
                    cell[0][2] = chr(9559)

            if (val >> 1) & 1 and (val >> 0) & 1 and j != (width - 1):

                if (grid[i][j+1] >> 0 & 1):
                    cell[0][2] = '╦'
                else:
                    cell[0][2] = chr(9559)


            new_grid[i][j] = cell
    
    return new_grid

#just for testing
def print_final_grid(grid: npt.NDArray) -> None:

    height, width = grid.shape

    for row in range(height):
        for index1 in range(3):
            line = ''
            for col in range(width):
                cell = grid[row][col]
                for index2 in range(5):
                    line += str(cell[index1][index2])
            print(line)




if __name__ == '__main__':

    SIZE  = (12, 12)
    SEED  = 42
    ENTRY = (0, 0)
    EXIT  = (2, 3)

    maze_gen = MazeGenerator(SIZE, SEED)
    mat = maze_gen.generate(ENTRY, EXIT)
    mat = maze_gen.paint_42(mat)
    mat = np.where(mat == 15, BARRIER, MODIFIABLE)

    print('Kruskal (algo1)')
    try:
        new_mat = mazegen_perfect.fill(mat, ENTRY, EXIT, algorithm='algo1', seed=SEED)
    except ValueError as e:
        print(e)

    print(new_mat)
    new_mat = get_cell_matrix(new_mat)

    print_final_grid(new_mat)
