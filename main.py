from mazegen_pkg import MazeGenerator, save_maze_to_txt, save_ber


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


def check_file_name(file_name: str) -> str:

    point: int = 0
    for letter in file_name:
        if letter == '.':
            point = point + 1
        if (not letter.isalnum and not letter == '.' and not letter == '_') or point > 1:
            return "INVALID!"
    if file_name.endswith(".ber"):
        return "ber"
    elif file_name.endswith(".txt"):
        return "txt"
    else:
        return "GOOD TRY, BUT STILL INVALID!"    


def main() -> None:

    maze_gen = MazeGenerator()
    maze = maze_gen.generate_maze()
    colours = maze_gen.MazeColours()
    maze_gen.maze_animate(maze, colours)
    solv_bool = False
    save_file: str = check_file_name(maze_gen.output)
    while True:

        try:
            option = int(input("Select option: \n1: Toggle Solution\n2: Choose Colours\n3: Regenerate Maze\n4: Change Seed Manually\n5: Save \n6: Exit\n"))
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
                print(f"{maze_gen.seed}")
                seed: int = int(input("New Seed: "))
                maze_gen.seed = seed
                print(f"{maze_gen.seed}")
                maze = maze_gen.generate_maze()
            if option == 5:
                if save_file == "txt":
                    save_maze_to_txt(maze, maze_gen.entry, maze_gen.exit_coord, maze_gen.output)
                elif save_file == "ber":
                    save_ber(maze, maze_gen.entry, maze_gen.exit_coord, maze_gen.output)
                else:
                    print("Invalid output file name provided")
            if option == 6:
                exit()
        except Exception as e:
            print(e)
        except KeyboardInterrupt as k:
            print(k)


if __name__ == '__main__':
    main()
