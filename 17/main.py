import fileinput
from functools import cache
from math import inf
from pathlib import Path
from heapq import heappop, heappush

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    grid = []
    for line in get_input():
        grid.append([int(c) for c in line])
    return grid


def solve1(matrix):
    rows, cols = len(matrix), len(matrix[0])
    heap = [(0, 0, 0, 5, 0)]  # (cost, x, y, direction, steps)
    visited = set()
    min_cost = inf

    # directions: 0 = up, 1 = right, 2 = down, 3 = left
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    while heap:
        cost, x, y, direction, steps = heappop(heap)

        if x == rows - 1 and y == cols - 1:
            min_cost = cost
            break

        for i in range(4):
            # ignore reverse direction
            if (i + 2) % 4 == direction:
                continue

            nx, ny = x + dx[i], y + dy[i]
            nsteps = steps + 1 if direction == i else 1

            # valid move
            if 0 <= nx < rows and 0 <= ny < cols and nsteps <= 3:
                state = (nx, ny, i, nsteps)

                if state not in visited:
                    visited.add(state)
                    heappush(heap, (cost + matrix[nx][ny], nx, ny, i, nsteps))

    # print(len(visited))
    return min_cost


def solve2(matrix):
    rows, cols = len(matrix), len(matrix[0])
    heap = [(0, 0, 0, 5, 10)]  # (cost, x, y, direction, steps)
    visited = set()
    min_cost = inf

    # directions: 0 = up, 1 = right, 2 = down, 3 = left
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    while heap:
        cost, x, y, direction, steps = heappop(heap)

        if x == rows - 1 and y == cols - 1:
            min_cost = cost
            break

        for i in range(4):
            # ignore reverse direction
            if (i + 2) % 4 == direction:
                continue

            if i != direction and steps < 4:
                continue

            nx, ny = x + dx[i], y + dy[i]
            nsteps = steps + 1 if direction == i else 1

            # valid move
            if 0 <= nx < rows and 0 <= ny < cols and nsteps <= 10:
                state = (nx, ny, i, nsteps)

                if state not in visited:
                    visited.add(state)
                    heappush(heap, (cost + matrix[nx][ny], nx, ny, i, nsteps))

    # print(len(visited))
    return min_cost


@cache
def q1():
    grid = parse()
    return solve1(grid)


@cache
def q2():
    grid = parse()
    return solve2(grid)


def main():
    print(q1())
    print(q2())
    assert q1() == 817
    assert q2() == 925


if __name__ == "__main__":
    main()
