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

main() {
    echo "Deleting ${DAY}"
    rm -r "${DAY_DIR}"
}

main
