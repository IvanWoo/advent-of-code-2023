import fileinput
from pathlib import Path
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"

EMPTY = 0
ROUND_ROCK = 1
CUBE_ROCK = -1
MAP = {"O": ROUND_ROCK, "#": CUBE_ROCK}


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    mat = []
    for line in get_input():
        mat.append([MAP.get(c, 0) for c in line])
    return np.mat(mat)


def tilt_north(old):
    (rows, cols) = old.shape
    new = np.zeros((rows, cols), dtype=int)
    for c in range(cols):
        new_c = []
        starting_pos = 0
        round_count = 0
        for r in range(rows):
            if old[r, c] == ROUND_ROCK:
                round_count += 1
            elif old[r, c] == CUBE_ROCK:
                new_c += (
                    [ROUND_ROCK] * round_count
                    + [EMPTY] * (r - starting_pos - round_count)
                    + [CUBE_ROCK]
                )
                round_count = 0
                starting_pos = r + 1
        new_c += [ROUND_ROCK] * round_count + [EMPTY] * (
            rows - starting_pos - round_count
        )
        new[:, c] = new_c
    return new


def tilt_west(old):
    return tilt_north(old.T).T


def tilt_south(old):
    return np.flipud(tilt_north(np.flipud(old)))


def tilt_east(old):
    return np.fliplr(tilt_west(np.fliplr(old)))


def tilt_cycle(old):
    new = old
    for fn in [tilt_north, tilt_west, tilt_south, tilt_east]:
        new = fn(new)
    return new


def get_total_loads(mat):
    rocks = ((mat == 1) * mat).sum(axis=1)
    loads = np.arange(len(mat), 0, -1)
    return sum(rocks * loads)


def q1():
    mat = parse()
    tilted_mat = tilt_north(mat)
    return get_total_loads(tilted_mat)


def q2():
    mat = parse()

    histories = []
    offset = 0
    repeat_len = 0
    while repeat_len == 0:
        histories.append(mat)
        new_mat = tilt_cycle(mat)
        for i, h in enumerate(histories):
            if (new_mat == h).all():
                offset = i
                repeat_len = len(histories) - i
                break
        mat = new_mat

    idx = offset + (int(1e9) - offset) % repeat_len
    final_mat = histories[idx]
    return get_total_loads(final_mat)


def main():
    print(q1())
    print(q2())
    assert q1() == 110677
    assert q2() == 90551


if __name__ == "__main__":
    main()
