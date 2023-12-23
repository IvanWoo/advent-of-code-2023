from collections import defaultdict
import fileinput
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


NEIGHBORS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


@cache
def q1():
    ret = 0
    inputs = list(get_input())
    rows, cols = len(inputs), len(inputs[0])
    for r in range(rows):
        num = ""
        is_part = False
        for c in range(cols):
            if inputs[r][c].isdigit():
                num += inputs[r][c]
                for dr, dc in NEIGHBORS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if inputs[nr][nc] != "." and not inputs[nr][nc].isdigit():
                            is_part = True
            else:
                if is_part:
                    ret += int(num)
                num = ""
                is_part = False
        if num and is_part:
            ret += int(num)
    return ret


@cache
def q2():
    gear_counter = defaultdict(list)
    inputs = list(get_input())
    rows, cols = len(inputs), len(inputs[0])
    for r in range(rows):
        num = ""
        gears = set()
        for c in range(cols):
            if inputs[r][c].isdigit():
                num += inputs[r][c]
                for dr, dc in NEIGHBORS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if inputs[nr][nc] == "*":
                            gears.add((nr, nc))
            else:
                for g in gears:
                    gear_counter[g].append(int(num))
                num = ""
                gears = set()
        if num:
            for g in gears:
                gear_counter[g].append(int(num))

    count = sum([v[0] * v[1] for v in gear_counter.values() if len(v) == 2])
    return count


def main():
    print(q1())
    print(q2())
    assert q1() == 532331
    assert q2() == 82301120


if __name__ == "__main__":
    main()
