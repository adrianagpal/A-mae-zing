from .rgb_text import rgb_text

"""
From our mazegen, we get the 42 constituted by 'F's.
We transform the 42 and edges into 255 (barrier).
"""
MODIFIABLE: int = 0xF
BARRIER:    int = 0xFF

"""
Bit 0 → N (0x1)   North wall
Bit 1 → E (0x2)   East  wall
Bit 2 → S (0x4)   South wall
Bit 3 → W (0x8)   West  wall
"""
N: int = 0x1
E: int = 0x2
S: int = 0x4
W: int = 0x8

NORTH: int = 0x1
EAST: int = 0x2
SOUTH: int = 0x4
WEST: int = 0x8

OPPOSITE: dict[int, int] = {N: S, S: N, E: W, W: E}
DIR_DELTA: dict[int, tuple[int, int]] = {
    N: (-1, 0), E: (0, 1), S: (1, 0), W: (0, -1)
}
DIR_CHAR: dict[int, str] = {N: 'N', E: 'E', S: 'S', W: 'W'}
DIRECTIONS: list[int] = [N, E, S, W]

WALL_BITS: list[int] = [NORTH, EAST, SOUTH, WEST]
WALL_CHARS: set[str] = {'═', '║', '╚', '╝', '╔', '╗', '╠', '╣', '╩', '╦', '╬'}

CHAR_DELTA: dict[str, tuple[int, int]] = {
    'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1),
}

SOLUTION_COLOUR: str = rgb_text('█', 255, 255, 0)
