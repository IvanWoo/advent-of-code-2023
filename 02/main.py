import fileinput
from functools import cache
from functools import reduce
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def count(subset: str):
    counter = defaultdict(int)
    for total, color in [x.strip().split() for x in subset.split(",")]:
        counter[color] = int(total)
    return counter


def is_possible(counter: defaultdict[str, int]):
    return counter["red"] <= 12 and counter["green"] <= 13 and counter["blue"] <= 14


def get_id_sum():
    ret = 0
    for line in get_input():
        game_id = int(line.split(":")[0].split()[1])
        record = line.split(":")[1]
        if all([is_possible(count(subset)) for subset in record.split(";")]):
            ret += game_id
    return ret


def get_power(counters: list[defaultdict]):
    least = defaultdict(int)
    for color in ["red", "green", "blue"]:
        for counter in counters:
            least[color] = max(least[color], counter[color])
    return reduce(lambda a, b: a * b, least.values(), 1)


def get_power_sum():
    ret = 0
    for line in get_input():
        record = line.split(":")[1]
        counters = [(count(subset)) for subset in record.split(";")]
        ret += get_power(counters)
    return ret


@cache
def q1():
    return get_id_sum()


@cache
def q2():
    return get_power_sum()


def main():
    print(q1())
    print(q2())
    assert q1() == 2207
    assert q2() == 62241


if __name__ == "__main__":
    main()
