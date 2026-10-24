#!/usr/bin/env bash
# Copy the game's web build (../next-token/build/web, made by its tools/export_web.sh) into site/game.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
src="${1:-$here/../next-token/build/web}"
rm -rf "$here/site/game"
mkdir -p "$here/site/game"
cp "$src"/index.* "$here/site/game/"
echo "copied $(du -sh "$here/site/game" | cut -f1) from $src"
