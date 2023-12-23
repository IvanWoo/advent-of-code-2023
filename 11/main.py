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
    image = []
    for line in get_input():
        image.append(list(line))

    rows, cols = len(image), len(image[0])
    rs, cs = set(), set()
    galaxies = []
    for r in range(rows):
        for c in range(cols):
            if image[r][c] == "#":
                galaxies.append((r, c))
                rs.add(r)
                cs.add(c)

    no_galaxy_rows = set(list(range(rows))) - rs
    no_galaxy_cols = set(list(range(cols))) - cs
    return image, galaxies, no_galaxy_rows, no_galaxy_cols


def dist(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_prefix_sum(n, no_galaxy_pos, scale):
    prefix_sum = [0] * n
    count = 0
    for r in range(n):
        if r in no_galaxy_pos:
            count += scale - 1
        prefix_sum[r] = count
    return prefix_sum


def get_ans(scale: int):
    image, galaxies, no_galaxy_rows, no_galaxy_cols = parse()

    rows, cols = len(image), len(image[0])
    prefix_sum_no_galaxy_rows = get_prefix_sum(rows, no_galaxy_rows, scale)
    prefix_sum_no_galaxy_cols = get_prefix_sum(cols, no_galaxy_cols, scale)

    expanded_galaxies = [
        (r + prefix_sum_no_galaxy_rows[r], c + prefix_sum_no_galaxy_cols[c])
        for r, c in galaxies
    ]

    # print(expanded_galaxies)
    ret = 0
    for i in range(len(expanded_galaxies)):
        for j in range(i, len(expanded_galaxies)):
            ret += dist(expanded_galaxies[i], expanded_galaxies[j])
    return ret


@cache
def q1():
    return get_ans(2)


@cache
def q2():
    return get_ans(int(1e6))


def main():
    print(q1())
    print(q2())
    assert q1() == 9965032
    assert q2() == 550358864332


if __name__ == "__main__":
    main()
