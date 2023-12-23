#!/user/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${BASE_DIR}/../config.sh"

if [ -z "${1:-}" ]; then
    printf "Usage: ${0} 42 \n"
    exit 1
fi

DAY="${1}"
DAY_DIR="${PROJECT_DIR}/${DAY}"

create_main_py() {
    cat >"${DAY_DIR}/main.py" <<EOF
import fileinput
from functools import cache
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"
def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()
@cache
def q1():
    pass
@cache
def q2():
    pass
def main():
    print(q1())
    # print(q2())
    # assert q1() == 42
    # assert q2() == 42
if __name__ == "__main__":
    main()
EOF
}

main() {
    echo "Creating new day ${DAY}"
    mkdir -p "${DAY_DIR}"
    create_main_py
    touch "${DAY_DIR}/input.txt"
}

main
