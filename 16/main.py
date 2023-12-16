import fileinput
from pathlib import Path
from collections import defaultdict, deque
import numpy as np
from functools import cache

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def pprint(rows, cols, visited):
    matrix = np.zeros((rows, cols))
    for pos in visited:
        matrix[pos] = 1
    print(matrix)


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


@cache
def parse():
    grid = []
    for line in get_input():
        grid.append(line)
    return grid


def move(pos: tuple[int, int], dir: tuple[int, int]):
    return (pos[0] + dir[0], pos[1] + dir[1]), dir


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def get_total(start_pos, start_dir):
    grid = parse()
    rows, cols = len(grid), len(grid[0])

    stack = deque([(start_pos, start_dir)])
    visited = defaultdict(set)

    while stack:
        pos, dir = stack.popleft()
        r, c = pos
        if not (0 <= r < rows and 0 <= c < cols):
            continue
        if dir in visited[pos]:
            continue

        visited[pos].add(dir)

        match grid[r][c]:
            case ".":
                stack.append(move(pos, dir))
            case "|":
                if dir in [LEFT, RIGHT]:
                    stack.append(move(pos, UP))
                    stack.append(move(pos, DOWN))
                else:
                    stack.append(move(pos, dir))
            case "-":
                if dir in [UP, DOWN]:
                    stack.append(move(pos, LEFT))
                    stack.append(move(pos, RIGHT))
                else:
                    stack.append(move(pos, dir))
            case "/":
                if dir == LEFT:
                    stack.append(move(pos, DOWN))
                elif dir == RIGHT:
                    stack.append(move(pos, UP))
                elif dir == UP:
                    stack.append(move(pos, RIGHT))
                elif dir == DOWN:
                    stack.append(move(pos, LEFT))
            case "\\":
                if dir == LEFT:
                    stack.append(move(pos, UP))
                elif dir == RIGHT:
                    stack.append(move(pos, DOWN))
                elif dir == UP:
                    stack.append(move(pos, LEFT))
                elif dir == DOWN:
                    stack.append(move(pos, RIGHT))
    # pprint(rows, cols, visited)
    return len(visited.keys())


def q1():
    return get_total((0, 0), RIGHT)


def q2():
    grid = parse()
    rows, cols = len(grid), len(grid[0])

    ret = 0
    for r in range(rows):
        ret = max(ret, get_total((r, 0), RIGHT))
        ret = max(ret, get_total((r, cols - 1), LEFT))
    for c in range(cols):
        ret = max(ret, get_total((0, c), DOWN))
        ret = max(ret, get_total((rows - 1, c), UP))

    return ret


def main():
    print(q1())
    print(q2())
    assert q1() == 6740
    assert q2() == 7041


if __name__ == "__main__":
    main()
