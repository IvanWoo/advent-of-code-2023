import fileinput
from functools import cache
from pathlib import Path

from tqdm import tqdm

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    raws = []
    aggs = []
    for line in get_input():
        r, a = line.split()
        raws.append(r)
        aggs.append([int(x) for x in a.split(",")])
    return raws, aggs


def is_valid(raw, agg):
    return [len(x) for x in raw.split(".") if x] == agg


def bitmask_iteration(length):
    for mask in range(1 << length):
        yield bin(mask)[2:].zfill(length)


def fill(raw, target_pos, bitmask):
    filled = [""] * len(raw)
    for tp, mask in zip(target_pos, bitmask):
        filled[tp] = "#" if mask == "1" else "."
    for i, c in enumerate(raw):
        if not filled[i]:
            filled[i] = c
    return "".join(filled)


# brute force
@cache
def q1_slow():
    raws, aggs = parse()
    ret = 0
    for raw, agg in tqdm(zip(raws, aggs)):
        target_pos = [i for i, v in enumerate(raw) if v == "?"]
        for bitmask in bitmask_iteration(len(target_pos)):
            filled = fill(raw, target_pos, bitmask)
            if is_valid(filled, agg):
                ret += 1
    return ret


@cache
def ways(s, sizes, curr_count=0) -> int:
    if not s:
        return not sizes and not curr_count

    total_ways = 0
    possibles = [".", "#"] if s[0] == "?" else s[0]
    for char in possibles:
        if char == "#":
            total_ways += ways(s[1:], sizes, curr_count + 1)
        else:
            if curr_count:
                if sizes and sizes[0] == curr_count:
                    total_ways += ways(s[1:], sizes[1:])
            else:
                total_ways += ways(s[1:], sizes)
    return total_ways


@cache
def q1_fast():
    raws, aggs = parse()
    return sum([ways(tuple(raw + "."), tuple(agg)) for raw, agg in zip(raws, aggs)])


@cache
def q1():
    return q1_fast()


@cache
def q2():
    raws, aggs = parse()
    return sum(
        [
            ways(tuple("?".join([raw] * 5) + "."), tuple(agg * 5))
            for raw, agg in zip(raws, aggs)
        ]
    )


def main():
    print(q1())
    print(q2())
    assert q1() == 7490
    assert q2() == 65607131946466


if __name__ == "__main__":
    main()
