import fileinput
from functools import cache
from pathlib import Path
from collections import Counter, defaultdict

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def parse():
    hands, bets = [], []
    for line in get_input():
        hand, bet = line.split()
        hands.append(hand)
        bets.append(int(bet))
    return hands, bets


def classify(hands, counter):
    ret = defaultdict(list)
    for i, hand in enumerate(hands):
        c = counter(hand)
        if 5 in c:
            ret[5].append((hand, i))
        elif 4 in c:
            ret[4].append((hand, i))
        elif 3 in c and 2 in c:
            ret[32].append((hand, i))
        elif 3 in c:
            ret[3].append((hand, i))
        elif Counter(c)[2] == 2:
            ret[22].append((hand, i))
        elif 2 in c:
            ret[2].append((hand, i))
        else:
            ret[1].append((hand, i))
    return ret


def translate(hand: str, rule: str) -> tuple:
    rule_map = {x.strip(): i for i, x in enumerate(reversed(rule.split(",")))}
    return tuple([rule_map[c] for c in hand])


def get_ranks(hands, counter, rule):
    n = len(hands)
    classified_hands = classify(hands, counter)
    sorted_hands = []
    for klass in [5, 4, 32, 3, 22, 2, 1]:
        same_class_hands = classified_hands[klass]
        if not same_class_hands:
            continue
        sorted_same_class_hands = sorted(
            same_class_hands, reverse=True, key=lambda x: translate(x[0], rule)
        )
        sorted_hands.extend(sorted_same_class_hands)
    return list(zip(sorted_hands, reversed(range(1, n + 1))))


def get_total_winning(counter, rule):
    hands, bets = parse()
    ranks = get_ranks(hands, counter, rule)

    ret = 0
    for h_i, r in ranks:
        _, i = h_i
        ret += r * bets[i]
    return ret


@cache
def q1():
    def counter(hands):
        c = Counter(hands)
        return list(c.values())

    rule = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2"

    return get_total_winning(counter, rule)


@cache
def q2():
    def counter(hands):
        c = Counter(hands)
        total_wildcard = c["J"]
        c["J"] = 0
        c[c.most_common(1)[0][0]] += total_wildcard
        return list(c.values())

    rule = "A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J"

    return get_total_winning(counter, rule)


def main():
    print(q1())
    print(q2())
    assert q1() == 253910319
    assert q2() == 254083736


if __name__ == "__main__":
    main()
