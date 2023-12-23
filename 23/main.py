import fileinput
from math import inf
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    maze = [line for line in get_input()]
    return maze


maze = parse()
rows, cols = len(maze), len(maze[0])
start = 0, 1
end = rows - 1, cols - 2


# edge contraction
def get_points():
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    points = [start, end]
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == "#":
                continue
            neighbors = 0
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#":
                    neighbors += 1
            if neighbors >= 3:
                points.append((r, c))
    return points


def get_graph(dirs):
    points = get_points()
    graph = {pt: {} for pt in points}
    for sr, sc in points:
        stack: list[tuple[int, int, int]] = [(sr, sc, 0)]
        seen = {(sr, sc)}

        while stack:
            r, c, n = stack.pop()
            if n != 0 and (r, c) in points:
                graph[(sr, sc)][(r, c)] = n
                continue

            for dr, dc in dirs[maze[r][c]]:
                nr, nc = dr + r, dc + c
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and maze[nr][nc] != "#"
                    and (nr, nc) not in seen
                ):
                    stack.append((nr, nc, n + 1))
                    seen.add((nr, nc))
    return graph


def q1():
    dirs = {
        ">": [(0, 1)],
        "<": [(0, -1)],
        "^": [(-1, 0)],
        "v": [(1, 0)],
        ".": [(-1, 0), (1, 0), (0, -1), (0, 1)],
    }
    graph = get_graph(dirs)

    seen = set()

    # backtrack
    def dfs(pt):
        if pt == end:
            return 0

        ret = -inf
        seen.add(pt)
        for n_pt, distance in graph[pt].items():
            if n_pt not in seen:
                ret = max(ret, dfs(n_pt) + distance)
        seen.remove(pt)
        return ret

    return dfs(start)


def q2():
    dirs = {c: [(-1, 0), (1, 0), (0, -1), (0, 1)] for c in "><^v."}
    graph = get_graph(dirs)

    seen = set()

    # backtrack
    def dfs(pt):
        if pt == end:
            return 0

        ret = -inf
        seen.add(pt)
        for n_pt, distance in graph[pt].items():
            if n_pt not in seen:
                ret = max(ret, dfs(n_pt) + distance)
        seen.remove(pt)
        return ret

    return dfs(start)


def main():
    print(q1())
    print(q2())
    assert q1() == 2238
    assert q2() == 6398


if __name__ == "__main__":
    main()
