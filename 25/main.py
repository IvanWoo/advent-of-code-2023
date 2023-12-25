import fileinput
from collections import defaultdict, deque
from functools import cache
from pathlib import Path

import graphviz
import networkx as nx

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    connections = defaultdict(set)
    for line in get_input():
        head, tail = line.split(": ")
        for nxt in tail.split():
            connections[head].add(nxt)
    return connections


def render(connections):
    # Create a new undirected graph
    g = graphviz.Graph("G", filename="graph.gv", engine="neato")
    g.attr(overlap="false")
    for u, vs in connections.items():
        for v in vs:
            g.edge(u, v)
    g.render("25/25", format="gv")


def q1_eyeball():
    connections = parse()
    render(connections)
    """
    disconnect these three by observing the graphviz
    zlv - bmx
    lrd - qpg
    xsl - tpb
    """
    try:
        for u, v in [("zlv", "bmx"), ("lrd", "qpg"), ("xsl", "tpb")]:
            connections[u].remove(v)
            connections[v].remove(u)
    except KeyError:
        ...
    total = len(connections.keys())
    seen = set()
    q = deque(["gts"])
    while q:
        curr = q.popleft()
        if curr not in seen:
            seen.add(curr)

        for nxt in connections[curr]:
            if nxt not in seen:
                q.append(nxt)
    # print(len(seen))
    return (total - len(seen)) * len(seen)


def _q1():
    connections = parse()
    g = nx.Graph()
    for u, vs in connections.items():
        for v in vs:
            g.add_edge(u, v)
    g.remove_edges_from(nx.minimum_edge_cut(g))
    a, b = nx.connected_components(g)
    return len(a) * len(b)


@cache
def q1():
    return _q1()


def main():
    print(q1())
    assert q1() == 559143


if __name__ == "__main__":
    main()
