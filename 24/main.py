import fileinput
from dataclasses import astuple, dataclass
from functools import cache
from math import inf
from pathlib import Path

import numpy as np
from scipy.linalg import solve
from z3 import Int, Ints, Solver, sat

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


@dataclass(frozen=True)
class Position:
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Velocity:
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Hailstone:
    position: Position
    velocity: Velocity


def parse():
    hailstones = []
    for line in get_input():
        p, v = line.split(" @ ")
        hailstones.append(
            Hailstone(
                Position(*[int(c) for c in p.split(",")]),
                Velocity(*[int(c) for c in v.split(",")]),
            )
        )
    return hailstones


def calculate_intercept(x, y, k):
    return y - k * x


def calculate_intersection(k1, b1, k2, b2):
    """
    solve equations: y = k1*x + b1, y = k2*x + b2
    [
        -k1*x + y = b1,
        -k2*x + y = b2,
    ]
    """
    if k1 == k2:
        return (inf, inf)
    A = np.array([[-k1, 1], [-k2, 1]])  # Coefficients
    b = np.array([b1, b2])  # Constants on the right

    # Solve the system:
    x, y = solve(A, b)
    return (x, y)


def is_valid(h1: Hailstone, h2: Hailstone) -> bool:
    k1 = h1.velocity.y / h1.velocity.x
    b1 = calculate_intercept(h1.position.x, h1.position.y, k1)
    k2 = h2.velocity.y / h2.velocity.x
    b2 = calculate_intercept(h2.position.x, h2.position.y, k2)
    ix, iy = calculate_intersection(k1, b1, k2, b2)
    is_in_range = (
        200000000000000 <= ix <= 400000000000000
        and 200000000000000 <= iy <= 400000000000000
    )
    if is_in_range:
        t1 = (ix - h1.position.x) / h1.velocity.x
        t2 = (ix - h2.position.x) / h2.velocity.x
        return t1 >= 0 and t2 >= 0
    return False


@cache
def q1():
    hailstones = parse()
    count = 0
    for i in range(len(hailstones)):
        for j in range(i, len(hailstones)):
            if is_valid(hailstones[i], hailstones[j]):
                count += 1
    return count


def z3_solve(data):
    # defining the variables
    px, py, pz, vx, vy, vz = Ints("px py pz vx vy vz")

    # create the solver
    s = Solver()

    # for each hailstone in the data
    for i, ((hx, hy, hz), (vhx, vhy, vhz)) in enumerate(data):
        # create a variable for the time of collision
        ti = Int(f"t_{i}")
        # add the equations for the collision
        s.add(hx + vhx * ti == px + vx * ti)
        s.add(hy + vhy * ti == py + vy * ti)
        s.add(hz + vhz * ti == pz + vz * ti)
        s.add(ti >= 0)

    # check if the problem is solvable
    if s.check() == sat:
        # get the solution
        m = s.model()
        return sum(m[coord].as_long() for coord in [px, py, pz])


@cache
def q2():
    hailstones = parse()
    data = [astuple(h) for h in hailstones]
    return z3_solve(data)


def main():
    print(q1())
    print(q2())
    assert q1() == 23760
    assert q2() == 888708704663413


if __name__ == "__main__":
    main()
