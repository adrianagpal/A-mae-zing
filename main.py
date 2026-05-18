import sys
import numpy.typing as npt
from mazegen_pkg import MazeGenerator


#just for testing
def print_final_grid_np(grid: npt.NDArray) -> None:

    height, width = grid.shape

    for row in range(height):
        for index1 in range(3):
            line = ''
            for col in range(width):
                cell = grid[row][col]
                for index2 in range(5):
                    line += str(cell[index1][index2])
            print(line)
           
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

def print_grid(grid: list[list[int]], label: str = '') -> None:
    if label:
        print(f"\n{label}")
        print('-' * (len(grid[0]) * 3))
    r = 0
    while r < len(grid):
        c = 0
        cells = []
        while c < len(grid[r]):
            cells.append('F' if grid[r][c] == 0xFF else f'{grid[r][c]:X}')
            c += 1
        print(''.join(cells))
        r += 1

def main() -> None:

    maze_gen = MazeGenerator()
    maze = maze_gen.generate_maze()

    colours = maze_gen.MazeColours()
    maze_gen.maze_animate(maze, colours)
    solv_bool = False
    while True:

        try:
            option = int(input("Select option: \n1: toggle solution\n2: choose colours\n3: Regenerate maze\n4: Exit\n"))
            if option == 1 and solv_bool == False:
                maze_gen.maze_solve(maze, colours)
                solv_bool = True
            elif option == 1 and solv_bool == True:
                maze_gen.maze_renderer(maze, colours)
                solv_bool = False
            if option == 2:
                colours.ask_colours()
                maze = maze_gen.generate_maze()
                maze_gen.maze_renderer(maze, colours)
            if option == 3:
                maze_gen.maze_animate(maze, colours)
                solv_bool = False
            if option == 4:
                exit()
        except Exception as e:
            print(e)
        except KeyboardInterrupt as k:
            print(k)

if __name__ == '__main__':
    main()
