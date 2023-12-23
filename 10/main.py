import fileinput
from functools import cache
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


tile_map = {
    "|": ["n", "s"],
    "-": ["e", "w"],
    "L": ["n", "e"],
    "J": ["n", "w"],
    "7": ["s", "w"],
    "F": ["s", "e"],
    ".": [],
    "S": ["n", "s", "e", "w"],
}

tile_map = {k: sorted(v) for k, v in tile_map.items()}

dir_map = {
    "n": (-1, 0),
    "s": (1, 0),
    "w": (0, -1),
    "e": (0, 1),
}


def reverse_dict(d):
    return {tuple(v): k for k, v in d.items()}


tile_map_rev = reverse_dict(tile_map)
dir_map_rev = reverse_dict(dir_map)

connect_map = {"n": "s", "s": "n", "e": "w", "w": "e"}


def parse():
    maze = [line for line in get_input()]
    rows, cols = len(maze), len(maze[0])
    starting = (0, 0)

    connections: dict[tuple, set[tuple[int, int]]] = defaultdict(set)
    for r in range(rows):
        for c in range(cols):
            curr = maze[r][c]
            if curr == "S":
                starting = (r, c)
                continue
            for curr_dir in tile_map[curr]:
                required_neighbor_dir = connect_map[curr_dir]
                dr, dc = dir_map[curr_dir]
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor = maze[nr][nc]
                    if required_neighbor_dir in tile_map[neighbor]:
                        connections[(r, c)].add((nr, nc))
                        connections[(nr, nc)].add((r, c))
    return maze, starting, connections


def pprint(grid):
    for row in grid:
        print("".join(row))
    print()


@cache
def q1():
    maze, starting, connections = parse()
    rows, cols = len(maze), len(maze[0])
    # print(connections)
    ans = 0
    grid = [["." for _ in range(cols)] for _ in range(rows)]

    stack = [starting]
    steps = 0
    while stack:
        new_stack = []
        for curr in stack:
            r, c = curr
            if grid[r][c] != ".":
                continue
            grid[r][c] = str(steps)
            ans = max(ans, steps)
            new_stack.extend(connections[curr])
        stack = new_stack
        steps += 1
    # pprint(grid)
    return ans


def identify_staring_pipe(starting, connections):
    r, c = starting
    dirs = []
    for tr, tc in connections[starting]:
        dir = dir_map_rev[((tr - r), (tc - c))]
        dirs.append(dir)
    pipe = tile_map_rev[tuple(sorted(dirs))]
    return pipe


@cache
def q2():
    MAIN_LOOP = "="
    INSIDE = "I"
    OUTSIDE = "O"

    # ray casting algorithm
    # https://en.wikipedia.org/wiki/Point_in_polygon
    def count_horizontal(r, c, maze, grid):
        count = 0
        for k in range(c):
            if grid[r][k] != MAIN_LOOP:
                continue
            count += maze[r][k] in {"J", "L", "|"}
        return count

    maze, starting, connections = parse()
    rows, cols = len(maze), len(maze[0])

    staring_pipe = identify_staring_pipe(starting, connections)
    # print(staring_pipe)
    maze[starting[0]] = maze[starting[0]].replace("S", staring_pipe)

    grid = [["." for _ in range(cols)] for _ in range(rows)]

    stack = [starting]
    while stack:
        new_stack = []
        for curr in stack:
            r, c = curr
            if grid[r][c] != ".":
                continue
            grid[r][c] = MAIN_LOOP
            new_stack.extend(connections[curr])
        stack = new_stack
    # pprint(grid)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != ".":
                continue
            count = count_horizontal(r, c, maze, grid)
            if count % 2 == 1:
                grid[r][c] = INSIDE
            else:
                grid[r][c] = OUTSIDE
    # pprint(maze)
    # pprint(grid)
    ans = sum([1 for r in range(rows) for c in range(cols) if grid[r][c] == INSIDE])
    return ans


def main():
    print(q1())
    print(q2())
    assert q1() == 6823
    assert q2() == 415


if __name__ == "__main__":
    main()
