_This project has been created as part of the 42 curriculum by Arianag and Apalese-_

# Description

A-Maze-Ing is, on the surface, a project about coding a maze generator, and it is. But the real focus of the project is to show how to generate your own non-trivial package.

There are some guidelines on how the map should be codified: it is a grid of hexadecimal values from 0 to 15, the first one being an open cell with no walls around it, and `F` being a fully closed cell with no communications to the surrounding ones. Additionally, `42` should be stamped on the maze in the form of unconnected `F`-valued cells.

We decided to add some animations around the maze building. They do not represent the actual steps the algorithm takes; they are only generic animations. However, we also animated the solution path between entry and exit.

There is an option to change the seed from the config file, allowing new maps to be generated with the same parameters. Exported maps will use the current seed, not the config one if it was changed during execution.

Exporting maps also includes a "secret" feature where it can build a `.ber` map retro-compatible with the old CC project `So_Long`. To unlock this functionality, simply change the naming of your output file to a `.ber` extension in the config file.

## Algorithms Used

### Prim's

This one starts at a random cell and checks for any non-added cell at its borders, breaking open a path to it. After some iterations, every cell has been accessed and the maze is generated.

It expands from a random point like "tentacles" until they reach every point.

### Kruskal's

We also start with a random cell and join it to another block on its frontiers. Then we select another block and connect it to a neighbouring block. Once all blocks are one and the same, the maze has been generated.

It merges many groups together until every cell is part of one conjoined block.

Both algorithms only make perfect mazes. To make them imperfect, we do a BFS from entry and exit, looking for a cell that would touch the other's path if not for a wall between them, and then break it. Since we already had a path between the entry and exit, generating a second one creates a non-trivial loop in the maze.

## Reusability

The algorithms were written with redundancy in mind. Some helper functions are shared between them, meaning any future implementation for a third generator would also benefit from part of the common logic.

Maze generation also allows for any pattern to be stamped on it, so changing the `42` for something else would not require any major refactoring.

---

# Instructions

To run the program, you can simply execute the rule:

```bash
make run
```

This will call the main program with the `config.txt` from the same root directory. Alternatively, you can manually call your interpreter with the main program and pass the `config.txt` as the only argument.

Once in the program, you will have some numbered options to interact with:

1. Toggle the solution display, either hiding or showing it.
2. Set the RGB values to redefine the colour for the walls and the barrier that forms the `42` logo.
3. Regenerate the maze with the current colour values and seed.
4. Manually set a new seed to override the one given in `config.txt` for the next generation.
5. Save the current map as a `.txt` or a `.ber` file compatible with the `so_long` project.
6. Close the program.

To generate a package that you can later import into a new project, you can run:

```bash
make pack
```

This will install dependencies and build the package for you. The `.whl` file will be inside the newly created `dist` directory.

---

# Configuration File

Keys in the configuration must all be present and not duplicated, caps are not strict. Their usage is as follows:

```txt
WIDTH=         int value (less than or equal to 100 recommended, but not enforced)

HEIGHT=        int value (less than or equal to 27 recommended, but not enforced)

ENTRY=         coordinate for the entry. It cannot overlap the outside border
               or the 42 barrier. Two values inside the border with a single comma in between.
               Example: "42,42"

EXIT=          coordinate for the exit. It cannot overlap the outside border
               or the 42 barrier. Two values inside the border with a single comma in between.
               Example: "42,42"

OUTPUT_FILE=   a valid name for the output file. It should end in .txt.
               Additionally, as a "secret" feature, using .ber as the extension
               will save the maze as a so_long compatible file.

PERFECT=       either "True" or "False"

SEED=          a numeric seed used for maze generation

ALGORITHM=     currently only "Kruskal" and "Prim" are supported
```

---

# Resources

- https://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm
- https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm

---

# Role Delegation

## Adrianag

- Parsing
- Maze Rendering
- Map Storing
- `mypy` and `flake8` compliance

## Apalese

- Algorithm Implementations
- Animations
