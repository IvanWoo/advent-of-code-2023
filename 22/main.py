import fileinput
from pathlib import Path
from collections import deque

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    bricks = []
    for line in get_input():
        bricks.append(list(map(int, line.replace("~", ",").split(","))))
    return bricks


def overlap(a, b):
    return max(a[0], b[0]) <= min(a[3], b[3]) and max(a[1], b[1]) <= min(a[4], b[4])


def get_support_maps():
    bricks = parse()
    bricks.sort(key=lambda b: b[2])

    for i, b in enumerate(bricks):
        max_z = 1
        for check in bricks[:i]:
            if overlap(check, b):
                max_z = max(max_z, check[5] + 1)

        b[5] -= b[2] - max_z
        b[2] = max_z

    bricks.sort(key=lambda b: b[2])
    # print(bricks)

    # x supports
    support = {i: set() for i in range(len(bricks))}

    # x is supported by
    supported = {i: set() for i in range(len(bricks))}

    for j, upper in enumerate(bricks):
        for i, lower in enumerate(bricks[:j]):
            if overlap(upper, lower) and upper[2] == lower[5] + 1:
                support[i].add(j)
                supported[j].add(i)
    # print(support)
    # print(supported)
    return support, supported


def q1():
    bricks = parse()
    support, supported = get_support_maps()
    total = 0
    for i in range(len(bricks)):
        if all([len(supported[j]) >= 2 for j in support[i]]):
            total += 1
    return total


def q2():
    bricks = parse()
    support, supported = get_support_maps()
    total = 0
    for i in range(len(bricks)):
        fall = set()
        q = deque([i])
        while q:
            curr = q.popleft()
            fall.add(curr)

            for next in support[curr] - fall:
                if supported[next] <= fall:
                    fall.add(next)
                    q.append(next)
        total += len(fall) - 1
    return total


def main():
    print(q1())
    print(q2())
    assert q1() == 505
    assert q2() == 71002


if __name__ == "__main__":
    main()
