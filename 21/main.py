import fileinput
from functools import cache
from pathlib import Path
from copy import deepcopy
from collections import deque

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    maze = []
    for line in get_input():
        maze.append([c for c in line])

    rows, cols = len(maze), len(maze[0])
    (starting,) = [
        (r, c) for c in range(cols) for r in range(rows) if maze[r][c] == "S"
    ]
    return maze, starting


def pprint(maze, reachable):
    viz_maze = deepcopy(maze)
    for r, c in reachable:
        viz_maze[r][c] = "O"

    for row in viz_maze:
        print("".join(row))


maze, starting = parse()
sr, sc = starting
rows, cols = len(maze), len(maze[0])


def fill_slow(sr, sc, steps):
    curr_plots = [(sr, sc)]
    for _ in range(steps):
        next_plots = []
        # pprint(maze, curr_plots)
        visited = set()
        for r, c in curr_plots:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and maze[nr][nc] != "#"
                    and (nr, nc) not in visited
                ):
                    visited.add((nr, nc))
                    next_plots.append((nr, nc))
        curr_plots = next_plots
    return len(curr_plots)


def fill_fast(sr, sc, steps):
    ans = set()
    seen = {(sr, sc)}
    q = deque([(sr, sc, steps)])
    while q:
        r, c, s = q.popleft()

        if s % 2 == 0:
            ans.add((r, c))
        if s == 0:
            continue

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and maze[nr][nc] != "#"
                and (nr, nc) not in seen
            ):
                seen.add((nr, nc))
                q.append((nr, nc, s - 1))
    return len(ans)


def fill(sr, sc, steps):
    return fill_fast(sr, sc, steps)


@cache
def q1():
    steps = 64
    return fill(sr, sc, steps)


@cache
def q2():
    assert rows == cols
    size = rows
    steps = 26501365
    grid_width = steps // size - 1

    odd = (grid_width // 2 * 2 + 1) ** 2
    even = ((grid_width + 1) // 2 * 2) ** 2

    odd_points = fill(sr, sc, size * 2 + 1)
    even_points = fill(sr, sc, size * 2)

    corner_t = fill(size - 1, sc, size - 1)
    corner_r = fill(sr, 0, size - 1)
    corner_b = fill(0, sc, size - 1)
    corner_l = fill(sr, size - 1, size - 1)

    small_tr = fill(size - 1, 0, size // 2 - 1)
    small_tl = fill(size - 1, size - 1, size // 2 - 1)
    small_br = fill(0, 0, size // 2 - 1)
    small_bl = fill(0, size - 1, size // 2 - 1)

    large_tr = fill(size - 1, 0, size * 3 // 2 - 1)
    large_tl = fill(size - 1, size - 1, size * 3 // 2 - 1)
    large_br = fill(0, 0, size * 3 // 2 - 1)
    large_bl = fill(0, size - 1, size * 3 // 2 - 1)

    return sum(
        [
            odd * odd_points,
            even * even_points,
            corner_t,
            corner_r,
            corner_b,
            corner_l,
            (grid_width + 1) * (small_tr + small_tl + small_br + small_bl),
            grid_width * (large_tr + large_tl + large_br + large_bl),
        ]
    )


def main():
    print(q1())
    print(q2())
    assert q1() == 3687
    assert q2() == 610321885082978


if __name__ == "__main__":
    main()
