#!/usr/bin/env bash
# Refresh vendor/fragateiro-physics from a fragateiro checkout (read-only use of the game).
# Usage: scripts/sync-fragateiro.sh /path/to/fragateiro
set -euo pipefail
src="${1:?path to a fragateiro checkout}"
dest="$(cd "$(dirname "$0")/.." && pwd)/vendor/fragateiro-physics"
rm -rf "$dest"
mkdir -p "$dest"
cp -r "$src/src/physics/." "$dest/"
echo "$(git -C "$src" rev-parse HEAD) ($(git -C "$src" log -1 --format=%cs))" > "$dest/SOURCE"
echo "Synced $(cat "$dest/SOURCE")"
