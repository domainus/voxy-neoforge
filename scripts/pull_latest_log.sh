#!/bin/bash
# Copy the latest Prism Launcher log into the repo for repeatable debugging.
# Usage: ./scripts/pull_latest_log.sh [destination]

set -euo pipefail

SOURCE_LOG="${VOXY_PULL_LATEST_LOG_SOURCE:-/var/home/ryan/.var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher/run/media/system/Warp_Core_Gamma/PrismaLauncher/instances/1.21.1/minecraft/logs/latest.log}"
DEST_LOG="${1:-.tmp/logs/latest-1.21.1.log}"

if [[ ! -f "$SOURCE_LOG" ]]; then
  echo "[ERROR] Prism latest.log not found: $SOURCE_LOG" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST_LOG")"
cp "$SOURCE_LOG" "$DEST_LOG"

DEST_DIR="$(cd "$(dirname "$DEST_LOG")" && pwd)"
DEST_ABS="$DEST_DIR/$(basename "$DEST_LOG")"

echo "[INFO] Copied Prism latest.log snapshot"
echo "source: $SOURCE_LOG"
echo "dest: $DEST_ABS"
