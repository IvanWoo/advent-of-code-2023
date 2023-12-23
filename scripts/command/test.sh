#!/user/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${BASE_DIR}/../config.sh"

for ((i = 1; i <= 24; i++)); do
    if ((i < 10)); then
        num="0$i" # prepend a leading zero for numbers less than 10
    else
        num="$i"
    fi

    target_file_path="$num/main.py"
    if [ -e "$target_file_path" ]; then
        echo "testing day $num..."
        pdm run $target_file_path
    else
        echo "$target_file_path does not exist."
    fi
done
