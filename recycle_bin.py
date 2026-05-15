#temporal thing to translate yours to mine, i was working with nested lists but was not really the same? idk
def from_mazegen(mat) -> list[list[int]]:
    rows = len(mat)#this should come from the config directly later
    cols = len(mat[0])
    grid: list[list[int]] = []
    r = 0
    while r < rows:
        row: list[int] = []
        c = 0
        while c < cols:
            row.append(BARRIER if mat[r][c] == 15 else MODIFIABLE)
            c = c + 1
        grid.append(row)
        r = r + 1
    return grid


def fill_bottom(grid: npt.NDArray, new_grid: npt.NDArray, i: int, j: int, idx_row: int, idx_col: int):

    cell = grid[i][j]
    if (
            cell & (SOUTH | WEST)
            and grid[i][j - 1] & SOUTH
        ):
        new_grid[idx_row + 1][idx_col - 1] = '╩'

    elif cell & (SOUTH | WEST):
        new_grid[idx_row + 1][idx_col - 1] = '╚'
    
    elif cell & SOUTH:
        new_grid[idx_row + 1][idx_col - 1] = '═'

    return new_grid

def fill_left(grid: npt.NDArray, new_grid: npt.NDArray, i: int, j: int, idx_row: int, idx_col: int):

    cell = grid[i][j]
    if (
            cell & (NORTH | EAST)
            and grid[i][j - 1] & EAST
        ):
        new_grid[idx_row - 1][idx_col + 1] = '╣'

    elif cell & (NORTH | EAST):
        new_grid[idx_row - 1][idx_col + 1] = '╗'
    
    elif cell & NORTH:
        new_grid[idx_row - 1][idx_col + 1] = '═'

    return new_grid


def upper_left_edge(grid: npt.NDArray, new_grid: npt.NDArray, i: int, j: int, idx_row: int, idx_col: int):

    cell = grid[i][j]
    if (
            cell & (NORTH | WEST) 
            and grid[i - 1][j - 1] & (SOUTH | EAST)
        ):
        new_grid[idx_row - 1][idx_col - 1] = '╬'

    elif (
            cell & (NORTH | WEST) 
            and grid[i - 1][j - 1] & SOUTH
        ):
        new_grid[idx_row - 1][idx_col - 1] = '╦'

    elif (
            cell & (NORTH | WEST) 
            and grid[i - 1][j - 1] & EAST
        ):
        new_grid[idx_row - 1][idx_col - 1] = '╠'

    elif (
            cell & NORTH
            and grid[i - 1][j - 1] & (SOUTH | EAST)
        ):
        new_grid[idx_row - 1][idx_col - 1] = '╩'

    elif cell & (NORTH | WEST):
        new_grid[idx_row - 1][idx_col - 1] = '╔'

    elif (
            cell & NORTH
            and grid[i - 1][j - 1] & EAST
        ):
        new_grid[idx_row - 1][idx_col - 1] = '╚'

    elif (
            cell & NORTH
            and grid[i - 1][j - 1] & SOUTH
        ):
        new_grid[idx_row - 1][idx_col - 1] = '═'

    elif (
            cell & WEST
            and grid[i - 1][j - 1] & (SOUTH | EAST)
        ):
        new_grid[idx_row - 1][idx_col - 1] = '╣'

    elif (
            cell & WEST
            and grid[i - 1][j - 1] & SOUTH
        ):
        new_grid[idx_row - 1][idx_col - 1] = '╗'

    elif (
            cell & WEST
            and grid[i - 1][j - 1] & EAST
        ):
        new_grid[idx_row - 1][idx_col - 1] = '║'

    return new_grid


def byte_intersection_bottom_left(cell, diagonal):

    byte = 0

    east = cell & SOUTH
    south = diagonal & EAST
    north = cell & WEST
    west = diagonal & NORTH

    if east:
        byte = byte | EAST
    if west:
        byte = byte | WEST
    if north:
        byte = byte | NORTH
    if south:
        byte = byte | SOUTH

    return byte

def debug_nibble():
    x = 13
    new_nibble = swap_nibbles(x)

    print(new_nibble)
    print(x >> 0 & 1)
    print(x >> 1 & 1)
    print(x >> 2 & 1)
    print(x >> 3 & 1)

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

def upper_left_edge(grid: npt.NDArray, new_grid: npt.NDArray, i: int, j: int, idx_row: int, idx_col: int):

    cell = grid[i][j]
    if (
            i > 0 and j > 0 
            and cell & (NORTH | WEST) 
            and grid[i - 1][j] & WEST 
            and grid[i][j - 1] & NORTH
        ):
        new_grid[idx_row - 1][idx_col - 1] = '╬'

    elif i > 0 and cell & (NORTH | WEST) and grid[i - 1][j] & WEST:
        new_grid[idx_row - 1][idx_col - 1] = '╠'

    elif j > 0 and cell & (NORTH | WEST) and grid[i][j - 1] & NORTH:
        new_grid[idx_row - 1][idx_col - 1] = '╦'

    elif cell & (NORTH | WEST):
        new_grid[idx_row - 1][idx_col - 1] = '╔'

    elif cell & NORTH:
        new_grid[idx_row - 1][idx_col - 1] = '═'

    return new_grid


def bottom_left_edge(grid: npt.NDArray, new_grid: npt.NDArray, i: int, j: int, idx_row: int, idx_col: int):

    cell = grid[i][j]
    if (
            j > 0
            and cell & (SOUTH | WEST)
            and grid[i][j - 1] & SOUTH
        ):
        new_grid[idx_row + 1][idx_col - 1] = '╩'

    elif cell & (SOUTH | WEST):
        new_grid[idx_row + 1][idx_col - 1] = '╚'
    
    elif cell & SOUTH:
        new_grid[idx_row + 1][idx_col - 1] = '═'

    return new_grid


def upper_right_edge(grid: npt.NDArray, new_grid: npt.NDArray, i: int, j: int, idx_row: int, idx_col: int):

    cell = grid[i][j]
    if (
            i > 0 and j > 0 
            and cell & (NORTH | EAST) 
            and grid[i - 1][j] & EAST 
            and grid[i][j + 1] & NORTH
        ):
        new_grid[idx_row - 1][idx_col + 1] = '╬'

    elif i > 0 and cell & (NORTH | EAST) and grid[i - 1][j] & EAST:
        new_grid[idx_row - 1][idx_col - 1] = '╣'

    elif j > 0 and cell & (NORTH | EAST) and grid[i][j + 1] & NORTH:
        new_grid[idx_row - 1][idx_col - 1] = '╦'

    elif cell & (NORTH | WEST):
        new_grid[idx_row - 1][idx_col - 1] = '╔'

    elif cell & NORTH:
        new_grid[idx_row - 1][idx_col - 1] = '═'

    return new_grid


def get_cell_matrix(grid: npt.NDArray):

    grid = np.pad(grid, pad_width=1, mode='constant', constant_values=15)
    height, width = grid.shape
    new_grid = np.full((2 * height + 1, 2 * width + 1), ' ', dtype=str)

    for i in range(height):

        for j in range(width):

            idx_row = i * 2 + 1
            idx_col = j * 2 + 1
            cell = grid[i][j]

            if cell & NORTH:
                new_grid[idx_row - 1][idx_col] = '═'
            if cell & EAST:
                new_grid[idx_row][idx_col + 1] = '║'
            if cell & WEST:
                new_grid[idx_row][idx_col - 1] = '║'
            if cell & SOUTH:
                new_grid[idx_row + 1][idx_col] = '═'

            new_grid = upper_left_edge(grid, new_grid, i, j, idx_row, idx_col)
            new_grid = bottom_left_edge(grid, new_grid, i, j, idx_row, idx_col)         
                       
            if cell == 255:
                new_grid[idx_row][idx_col] = '█'
       

    return new_grid


def get_cell_matrix(grid: npt.NDArray):

    height, width = grid.shape
    new_grid = np.full((2 * height + 1, 2 * width + 1), ' ', dtype=str)

    for i in range(height):

        for j in range(width):

            idx_row = i * 2 + 1
            idx_col = j * 2 + 1
            cell = grid[i][j]

            if cell & WEST:
                new_grid[idx_row][idx_col - 1] = '║'
                new_grid[idx_row + 1][idx_col - 1] = '║'

            if cell & EAST:
                new_grid[idx_row][idx_col + 1] = '║'
                new_grid[idx_row + 1][idx_col + 1] = '║'

            if (
                i > 0 and j > 0 
                and cell & (NORTH | WEST) 
                and grid[i - 1][j] & WEST 
                and grid[i][j - 1] & NORTH
            ):
                new_grid[idx_row - 1][idx_col - 1] = '╬'


            if cell & NORTH:
                new_grid[idx_row - 1][idx_col] = '═'

                if cell & WEST:
                    new_grid[idx_row - 1][idx_col - 1] = '╔'
                    
                    if j > 0 and grid[i][j - 1] & EAST:
                        new_grid[idx_row - 1][idx_col - 1] = '╦'

                        if i > 0 and j > 0 and grid[i - 1][j - 1] & EAST:
                            new_grid[idx_row - 1][idx_col - 1] = '╬'
                else:
                    new_grid[idx_row - 1][idx_col - 1] = '═'

                if cell & EAST:
                    new_grid[idx_row - 1][idx_col + 1] = '╗'
                    
                    if j < width - 1 and grid[i][j + 1] & WEST:
                        new_grid[idx_row - 1][idx_col + 1] = '╦'

                        if i > 0 and j < width - 1 and grid[i - 1][j + 1] & WEST:
                            new_grid[idx_row - 1][idx_col + 1] = '╬'
                else:
                    new_grid[idx_row - 1][idx_col + 1] = '═'
                
            if cell & SOUTH:
                new_grid[idx_row + 1][idx_col] = '═'

                if cell & WEST:
                    new_grid[idx_row + 1][idx_col - 1] = '╚'
                    
                    if j > 0 and grid[i][j - 1] & SOUTH:
                        new_grid[idx_row + 1][idx_col - 1] = '╩'

                        if i < height - 1 and grid[i + 1][j] & WEST:
                            new_grid[idx_row + 1][idx_col - 1] = '╬'

                else:
                    new_grid[idx_row + 1][idx_col - 1] = '═'

                if cell & EAST:
                    new_grid[idx_row + 1][idx_col + 1] = '╝'
                    
                    if j < width - 1 and grid[i][j + 1] & WEST:
                        new_grid[idx_row + 1][idx_col + 1] = '╩'

                        if i < height - 1 and grid[i + 1][j] & EAST:
                            new_grid[idx_row + 1][idx_col + 1] = '╬'

                else:
                    new_grid[idx_row + 1][idx_col + 1] = '═'
            
            if cell == 255:
                new_grid[idx_row][idx_col] = '█'
                
            

    return new_grid


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