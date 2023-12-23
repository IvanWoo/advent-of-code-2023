import fileinput
from functools import cache
import math
from pathlib import Path
from collections import deque, defaultdict
from dataclasses import dataclass

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"

BUTTON = "button"
ENTRYPOINT = "broadcaster"
FLIP_MODULE = "%"
CONJ_MODULE = "&"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


@dataclass(frozen=True)
class Module:
    name: str
    type: str
    destinations: list[str]


def parse() -> dict[str, Module]:
    modules = dict()
    for line in get_input():
        head, tail = line.split(" -> ")
        if head == ENTRYPOINT:
            type, key = "", head
        else:
            type, key = head[0], head[1:]
        modules[key] = Module(key, type, [c.strip() for c in tail.split(",")])
    return modules


def get_conjunction_modules_inputs_map(modules):
    conjunction_modules = [k for k, v in modules.items() if v.type == CONJ_MODULE]
    conjunction_modules_inputs_map = defaultdict(list)
    for k, v in modules.items():
        for cm in conjunction_modules:
            if cm in v.destinations:
                conjunction_modules_inputs_map[cm].append(k)
    return conjunction_modules_inputs_map


def pprint(start, pulse, end):
    # low, high: 0, 1
    print(f"{start} -{'low' if pulse == 0 else 'high'}-> {end}")


@cache
def q1():
    modules = parse()
    # print(modules)
    input_map = get_conjunction_modules_inputs_map(modules)
    # print(input_map)

    flip_states = {k: 0 for k, v in modules.items() if v.type == FLIP_MODULE}
    conj_states = {
        k: {i: 0 for i in input_map[k]}
        for k, v in modules.items()
        if v.type == CONJ_MODULE
    }
    # print(flip_states)
    # print(conj_states)
    pulse_count = [0, 0]
    for _ in range(1000):
        stack: deque[tuple[str, int, str]] = deque([(BUTTON, 0, ENTRYPOINT)])
        while stack:
            start, pulse, end = stack.popleft()
            # pprint(start, pulse, end)
            pulse_count[pulse] += 1
            if end not in modules:
                continue

            curr_module = modules[end]
            next_pulse = None
            match curr_module.type:
                case "":
                    next_pulse = pulse
                case "%":
                    if pulse == 0:
                        next_pulse = 1 ^ flip_states[end]
                        flip_states[end] ^= 1
                case "&":
                    conj_states[end][start] = pulse
                    next_pulse = any([x == 0 for x in conj_states[end].values()])

            if next_pulse is not None:
                for dest in curr_module.destinations:
                    stack.append((end, next_pulse, dest))
    return pulse_count[0] * pulse_count[1]


@cache
def q2():
    modules = parse()
    # print(modules)
    input_map = get_conjunction_modules_inputs_map(modules)
    # print(input_map)
    (feed,) = [name for name, module in modules.items() if "rx" in module.destinations]
    # print(feed)
    cycle_lengths = dict()
    seen = {name: 0 for name in input_map[feed]}

    flip_states = {k: 0 for k, v in modules.items() if v.type == FLIP_MODULE}
    conj_states = {
        k: {i: 0 for i in input_map[k]}
        for k, v in modules.items()
        if v.type == CONJ_MODULE
    }
    # print(flip_states)
    # print(conj_states)
    presses = 0
    while True:
        presses += 1
        stack: deque[tuple[str, int, str]] = deque([(BUTTON, 0, ENTRYPOINT)])
        while stack:
            start, pulse, end = stack.popleft()

            if end == feed and pulse == 1:
                seen[start] += 1
                if start not in cycle_lengths:
                    cycle_lengths[start] = presses
                else:
                    assert presses == seen[start] * cycle_lengths[start]

            if all(seen.values()):
                print(cycle_lengths)
                return math.lcm(*cycle_lengths.values())
            if end not in modules:
                continue

            curr_module = modules[end]
            next_pulse = None
            match curr_module.type:
                case "":
                    next_pulse = pulse
                case "%":
                    if pulse == 0:
                        next_pulse = 1 ^ flip_states[end]
                        flip_states[end] ^= 1
                case "&":
                    conj_states[end][start] = pulse
                    next_pulse = any([x == 0 for x in conj_states[end].values()])

            if next_pulse is not None:
                for dest in curr_module.destinations:
                    stack.append((end, next_pulse, dest))


def main():
    print(q1())
    print(q2())
    assert q1() == 680278040
    assert q2() == 243548140870057


if __name__ == "__main__":
    main()
