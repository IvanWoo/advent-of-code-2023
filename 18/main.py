import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


directions = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def parse():
    ops = []
    for line in get_input():
        dir, len, col = line.split()
        ops.append((dir, int(len), col[1:-1]))
    return ops


def solve(ops):
    x = y = 0
    points = [(0, 0)]
    b = 0
    for d, l, _ in ops:
        dx, dy = directions[d]
        x, y = x + dx * l, y + dy * l
        points.append((x, y))
        b += l

    # shoelace formula
    A = (
        abs(
            sum(
                points[i][0] * (points[i - 1][1] - points[(i + 1) % len(points)][1])
                for i in range(len(points))
            )
        )
        // 2
    )
    # Pick's theorem
    i = A - b // 2 + 1
    return i + b


def q1():
    ops = parse()
    return solve(ops)


def q2():
    ops = parse()
    updated_ops = []
    for _, _, color in ops:
        len, dir = int(color[1:-1], base=16), "RDLU"[int(color[-1])]
        updated_ops.append((dir, len, None))
    return solve(updated_ops)


def main():
    print(q1())
    print(q2())
    assert q1() == 35401
    assert q2() == 48020869073824


if __name__ == "__main__":
    main()
