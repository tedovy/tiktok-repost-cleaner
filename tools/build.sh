#!/bin/sh
# Packs the extension into dist/tiktok-repost-cleaner-v<version>.zip for a GitHub release.
set -e
cd "$(dirname "$0")/.."
VERSION=$(python3 -c "import json;print(json.load(open('manifest.json'))['version'])")
OUT="dist/tiktok-repost-cleaner-v$VERSION.zip"
mkdir -p dist
rm -f "$OUT"
zip -qr -X "$OUT" manifest.json background.js ready.js runner.js popup.html popup.css popup.js icons _locales LICENSE -x '*.DS_Store'
echo "$OUT"
