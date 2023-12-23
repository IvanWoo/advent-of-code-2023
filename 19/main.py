import fileinput
from collections import deque
from functools import cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse_workflow(s):
    name, tail = s[:-1].split("{")
    rules = tail.split(",")
    parsed_rules = []
    for r in rules:
        if ":" in r:
            condition, dest = r.split(":")
            parsed_rules.append((condition, dest))
        else:
            dest = r
            parsed_rules.append(("", dest))
    return {name: parsed_rules}


def parse_part(s):
    ret = {}
    for c in s[1:-1].split(","):
        key, value = c.split("=")
        ret[key] = int(value)
    return ret


def parse():
    data = {"workflows": [], "parts": [], "expanded_workflows": dict()}
    key = "workflows"
    for line in get_input():
        if not line:
            key = "parts"
            continue
        parsed = parse_workflow(line) if key == "workflows" else parse_part(line)
        data[key].append(parsed)

    data["expanded_workflows"] = {
        key: value
        for dictionary in data["workflows"]
        for key, value in dictionary.items()
    }
    return data


@cache
def q1():
    data = parse()
    workflows, parts = data["expanded_workflows"], data["parts"]
    ret = 0
    for p in parts:
        # print(p)
        curr = "in"
        while True:
            if curr in ["A", "R"]:
                break
            for condition, dest in workflows[curr]:
                if condition == "" or eval(condition, globals(), p):
                    curr = dest
                    break
        # print(curr)
        if curr == "A":
            ret += sum(p.values())
    return ret


RANGE = tuple[int, int]
RANGES = dict[str, RANGE]
MIN = 1
MAX = 4000


def get_intersection(r1: RANGE, r2: RANGE) -> RANGE:
    s_r1, s_r2 = sorted([r1, r2])
    if s_r1[1] < s_r2[0]:
        return (0, 0)
    return (s_r2[0], min(s_r1[1], s_r2[1]))


def get_combinations(ranges: RANGES) -> int:
    ret = 1
    for r in ranges.values():
        if not r[0]:
            ret *= 0
        else:
            ret *= r[1] - r[0] + 1
    return ret


def update_ranges(ranges: RANGES, category: str, constrain: RANGE) -> RANGES:
    new_ranges = {
        **ranges,
        **{category: get_intersection(ranges[category], constrain)},
    }
    return new_ranges


@cache
def q2():
    data = parse()
    workflows = data["expanded_workflows"]
    ret = 0
    stack: deque[tuple[str, dict[str, RANGE]]] = deque(
        [("in", {c: (MIN, MAX) for c in "xmas"})]
    )
    while stack:
        curr_wk, curr_ranges = stack.popleft()
        # print(curr_wk, curr_ranges)
        if not get_combinations(curr_ranges):
            continue

        if curr_wk in ["A", "R"]:
            if curr_wk == "A":
                # print(curr_ranges)
                # print(ret)
                ret += get_combinations(curr_ranges)
            continue

        new_ranges = {**curr_ranges}
        for condition, dest in workflows[curr_wk]:
            if "<" in condition:
                category, val = condition.split("<")
                stack.append(
                    (dest, update_ranges(new_ranges, category, (MIN, int(val) - 1)))
                )
                new_ranges = update_ranges(new_ranges, category, (int(val), MAX))
            elif ">" in condition:
                category, val = condition.split(">")
                stack.append(
                    (dest, update_ranges(new_ranges, category, (int(val) + 1, MAX)))
                )
                new_ranges = update_ranges(new_ranges, category, (MIN, int(val)))
            else:
                stack.append((dest, new_ranges))
    return ret


def main():
    print(q1())
    print(q2())
    assert q1() == 495298
    assert q2() == 132186256794011


if __name__ == "__main__":
    main()
