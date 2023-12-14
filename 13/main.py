import fileinput
from pathlib import Path
from typing import Callable

import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    matrixes = []
    curr = []
    for line in get_input():
        if not line:
            matrixes.append(np.matrix(curr))
            curr = []
        else:
            curr.append([1 if c == "#" else 0 for c in line])
    if curr:
        matrixes.append(np.matrix(curr))
    return matrixes


def is_mirror(m1: np.matrix, m2: np.matrix) -> bool:
    return np.all(np.flip(m1, axis=0) == m2)


def is_smudge(m1: np.matrix, m2: np.matrix) -> bool:
    return m1.size - (np.flip(m1, axis=0) == m2).sum() == 1


def summarize(m, scale, condition_func: Callable[[np.matrix, np.matrix], bool]):
    ret = 0
    rows, _ = m.shape
    for r in range(1, rows):
        dis = min(r, rows - r)
        if condition_func(m[(r - dis) : r], m[r : r + dis]):
            ret += r * scale
            break
    return ret


def q1():
    ret = 0
    matrixes = parse()
    for m in matrixes:
        # horizontal scan
        ret += summarize(m, 100, is_mirror)
        # vertical scan
        ret += summarize(m.T, 1, is_mirror)
    return ret


def q2():
    ret = 0
    matrixes = parse()
    for m in matrixes:
        # horizontal scan
        ret += summarize(m, 100, is_smudge)
        # vertical scan
        ret += summarize(m.T, 1, is_smudge)
    return ret


def main():
    print(q1())
    print(q2())
    assert q1() == 33356
    assert q2() == 28475


if __name__ == "__main__":
    main()
