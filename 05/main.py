import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def get_seeds(line):
    nums = [int(x) for x in line.split(":")[-1].split()]
    return nums


def get_map(content: str) -> list[tuple[int, int, int]]:
    m = []
    for line in content.split("\n"):
        if not line:
            continue
        m.append(tuple([int(x) for x in line.split()]))
    return m


def translate(seed: int, maps: list[list[tuple[int, int, int]]]) -> int:
    ret = seed
    for m in maps:
        temp = ret
        for dest, source, length in m:
            if source <= ret < source + length:
                temp = dest + ret - source
                break
        ret = temp
        # print(seed, ret, m)
    return ret


def parse():
    seeds = []
    maps: list[list[tuple[int, int, int]]] = []
    temp_map = ""
    for i, line in enumerate(get_input()):
        if i == 0:
            seeds = get_seeds(line)
            continue
        if not line:
            continue
        if "map" in line:
            if temp_map:
                maps.append(get_map(temp_map))
            temp_map = ""
            continue
        temp_map += line + "\n"
    if temp_map:
        maps.append(get_map(temp_map))
    return seeds, maps


def res_1():
    seeds, maps = parse()

    all_locations = [translate(s, maps) for s in seeds]
    # print(all_locations)
    return min(all_locations)


def is_in_range(seed, seeds):
    for i in range(0, len(seeds), 2):
        if seeds[i] <= seed < seeds[i] + seeds[i + 1]:
            return True
    return False


def res_2():
    seeds, maps = parse()

    new_maps = [
        [(source, dest, length) for dest, source, length in m] for m in maps[::-1]
    ]

    # maybe use numpy to vectorize this computation
    for min_loc in range(q1()):
        if min_loc % int(1e6) == 0:
            print(f"checkpoint: {min_loc}")
        potential_seed = translate(min_loc, new_maps)
        if is_in_range(potential_seed, seeds):
            return min_loc
    return -1


def q1():
    return res_1()


# takes around 18s
def q2():
    return res_2()


def main():
    print(q1())
    print(q2())
    assert q1() == 993500720
    assert q2() == 4917124


if __name__ == "__main__":
    main()
