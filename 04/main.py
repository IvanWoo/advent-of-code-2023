import fileinput
from collections import Counter, defaultdict
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse(line: str):
    meta, nums = line.split(":")
    card_id = int(meta.split()[-1])
    winning_nums, my_nums = nums.strip().split("|")
    w = Counter(winning_nums.split())
    m = Counter(my_nums.split())
    return card_id, w, m


@cache
def q1():
    total = 0
    for line in get_input():
        _, w, m = parse(line)
        matches = sum([1 for n in w if m[n] >= 1])
        total += 2 ** (matches - 1) if matches else 0
    return total


@cache
def q2():
    total = defaultdict(int)
    for line in get_input():
        card_id, w, m = parse(line)
        total[card_id] += 1
        matches = sum([1 for n in w if m[n] >= 1])
        for i in range(matches):
            total[card_id + i + 1] += total[card_id]
    return sum(total.values())


def main():
    print(q1())
    print(q2())
    assert q1() == 19855
    assert q2() == 10378710


if __name__ == "__main__":
    main()
