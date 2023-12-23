import fileinput
from functools import cache, reduce
from math import ceil, floor
from pathlib import Path

from sympy import solve, symbols

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"

x, t, d = symbols("x t d")


def get_solutions(t: int, d: int):
    solutions = solve(x**2 - t * x + d, x)
    return [ceil(min(solutions).evalf()), floor(max(solutions).evalf())]


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse_1():
    vals = []
    for line in get_input():
        vals.append([int(x) for x in line.split(":")[-1].split()])
    return vals


def parse_2():
    vals = []
    for line in get_input():
        vals.append(int("".join([x for x in line.split(":")[-1].split()])))
    return vals


@cache
def q1():
    times, distances = parse_1()
    n = len(times)
    counts = []
    for i in range(n):
        count = 0
        for hold in range(i, times[i]):
            if hold * (times[i] - hold) > distances[i]:
                count += 1
        counts.append(count)
    return reduce(lambda a, b: a * b, counts, 1)


# 2.5s
def _q2():
    time, distance = parse_2()
    count = 0
    for hold in range(time):
        if hold * (time - hold) > distance:
            count += 1
    return count


# 523.28 millis
def _q2_fast():
    time, distance = parse_2()
    solutions = get_solutions(time, distance)
    return min(time, solutions[1]) - solutions[0] + 1


@cache
def q2(fast=True):
    return _q2_fast() if fast else _q2()


def main():
    print(q1())
    print(q2())
    assert q1() == 6209190
    assert q2() == 28545089


if __name__ == "__main__":
    main()
