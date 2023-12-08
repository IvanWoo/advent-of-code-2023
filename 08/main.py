import fileinput
import math
from pathlib import Path
from itertools import cycle

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    instructions = ""
    nodes = dict()
    for i, line in enumerate(get_input()):
        if i == 0:
            instructions = line
            continue
        if not line:
            continue
        node, lr = [x.strip() for x in line.split("=")]
        nodes[node] = lr[1:-1].split(", ")
    return instructions, nodes


def q1():
    instruction, nodes = parse()
    steps = 0
    curr = "AAA"
    for ins in cycle(instruction):
        if curr == "ZZZ":
            break
        curr = nodes[curr][0 if ins == "L" else 1]
        steps += 1
    return steps


# brute force: too slow
def q2_slow():
    instructions, nodes = parse()
    curr_nodes = [node for node in nodes if node.endswith("A")]
    steps = 0
    for ins in cycle(instructions):
        if steps % int(1e6) == 0:
            print(f"checkpoint: {steps}")
        if all([n.endswith("Z") for n in curr_nodes]):
            break
        curr_nodes = [nodes[curr][0 if ins == "L" else 1] for curr in curr_nodes]
        steps += 1
    return steps


def q2():
    instructions, nodes = parse()
    curr_nodes = [node for node in nodes if node.endswith("A")]
    all_steps = []
    for curr in curr_nodes:
        steps = 0
        for ins in cycle(instructions):
            if curr.endswith("Z"):
                break
            curr = nodes[curr][0 if ins == "L" else 1]
            steps += 1
        all_steps.append(steps)
    return math.lcm(*all_steps)


def main():
    print(q1())
    print(q2())
    assert q1() == 19951
    assert q2() == 16342438708751


if __name__ == "__main__":
    main()
