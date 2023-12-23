import fileinput
from collections import defaultdict
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    raw = list(get_input())[0]
    return raw.split(",")


def _hash(string):
    ret = 0
    for char in string:
        ret += ord(char)
        ret *= 17
        ret %= 256
    return ret


def _sum(d: dict):
    ret = 0
    for i, (_, v) in enumerate(d.items()):
        ret += (i + 1) * int(v)
    return ret


@cache
def q1():
    sequence = parse()
    return sum([_hash(s) for s in sequence])


@cache
def q2():
    sequence = parse()
    hashmap = defaultdict(dict)
    for s in sequence:
        if "=" in s:
            key, val = s.split("=")
            hashmap[_hash(key)][key] = val
        elif "-" in s:
            key = s[:-1]
            if key in hashmap[_hash(key)]:
                del hashmap[_hash(key)][key]
    return sum([(k + 1) * _sum(v) for k, v in hashmap.items()])


def main():
    print(q1())
    print(q2())
    assert q1() == 497373
    assert q2() == 259356


if __name__ == "__main__":
    main()
