from mazegen import MazeGenerator, save_maze_to_txt, save_ber


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

    message = "Output file name is invalid"
    parts = file_name.split('.')
    if len(parts) != 2:
        return message

    for letter in file_name:
        if (
            not letter.isalnum() and
            not letter == '.' and
            not letter == '_'
        ):
            return message

    if file_name.endswith(".ber"):
        return "ber"
    elif file_name.endswith(".txt"):
        return "txt"
    else:
        return message


def main() -> None:

    maze_gen = MazeGenerator()
    maze = maze_gen.generate_maze()
    colours = maze_gen.MazeColours()
    maze_gen.maze_animate(maze, colours)
    solv_bool = False
    save_file: str = check_file_name(maze_gen.output)
    while True:

        try:
            print("=== A-Maze-ing ===")
            option = int(input("Select option: \n"
                               "1: Toggle Solution\n"
                               "2: Choose Colours\n"
                               "3: Regenerate Maze\n"
                               "4: Change Seed Manually\n"
                               "5: Save \n"
                               "6: Exit\n"
                               "Choice? (1-6): "))

            if option == 1 and not solv_bool:
                maze_gen.maze_solve(maze, colours)
                solv_bool = True
            elif option == 1 and solv_bool:
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
                    save_maze_to_txt(maze,
                                     maze_gen.entry,
                                     maze_gen.exit_coord, maze_gen.output)
                elif save_file == "ber":
                    save_ber(maze,
                             maze_gen.entry,
                             maze_gen.exit_coord, maze_gen.output)
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
