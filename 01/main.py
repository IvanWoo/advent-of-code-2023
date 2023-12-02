import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def get_num_1(line: str):
    nums = [c for c in line if c.isdigit()]
    head, tail = nums[0], nums[-1]
    return int(head + tail)


mapping = {
    **{
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    },
    **{str(v): v for v in range(1, 10)},
}


def get_num_2(line: str):
    head = min([(line.index(k), v) for k, v in mapping.items() if k in line])
    tail = max([(line.rindex(k), v) for k, v in mapping.items() if k in line])
    return head[1] * 10 + tail[1]


def q1():
    return sum([get_num_1(line) for line in get_input()])


def q2():
    return sum([get_num_2(line) for line in get_input()])


def main():
    print(q1())
    print(q2())
    assert q1() == 55477
    assert q2() == 54431


if __name__ == "__main__":
    main()
