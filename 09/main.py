import fileinput
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    rows = []
    for line in get_input():
        rows.append([int(x) for x in line.split()])
    return rows


def op(row):
    new_row = []
    for i in range(1, len(row)):
        new_row.append(row[i] - row[i - 1])
    return new_row


def get_seqs(row):
    seqs = []
    while True:
        seqs.append(row)
        row = op(row)
        if len(set(row)) == 1 and row[0] == 0:
            break
    return seqs


@cache
def q1():
    rows = parse()
    ret = 0
    for row in rows:
        seq = get_seqs(row)
        ret += sum([x[-1] for x in seq])
    return ret


@cache
def q2():
    rows = parse()
    ret = 0
    for row in rows:
        seq = get_seqs(row)
        ret += sum([x[0] * (1 if i % 2 == 0 else -1) for i, x in enumerate(seq)])
    return ret


def main():
    print(q1())
    print(q2())
    assert q1() == 1798691765
    assert q2() == 1104


if __name__ == "__main__":
    main()
