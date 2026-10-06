#!/usr/bin/env bash
# Запуск эмулятора на Linux и macOS.
# Все аргументы пробрасываются в python3 -m src.app.
#
# Примеры:
#   ./run.sh
#   ./run.sh --vfs /tmp/my_vfs
#   ./run.sh --vfs /tmp/my_vfs --script tests/start_script.txt

set -euo pipefail

cd "$(dirname "$0")"
python3 -m src.app "$@"