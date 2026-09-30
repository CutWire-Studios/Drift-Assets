#!/bin/sh
# Sets up the full build toolchain on a plain Ubuntu machine (CI runners, cloud dev boxes) without
# Drift's prebuilt Skia or the Blender flatpak:
#   - Blender 5.2 from blender.org into ~/.local/blender-5.2.2-linux-x64 (use DRIFT_BLENDER to point at it)
#   - ffmpeg with libwebp, and the libraries Blender needs, from apt
#   - .venv with Pillow
#   - build/skottie-render as a launcher for skottie-render.mjs (CanvasKit's Skottie in Node)
# Idempotent; run from anywhere. Needs root for apt (or sudo), Node 18+ and Python 3.
set -eu
REPO=$(cd "$(dirname "$0")/.." && pwd)
BLENDER_VERSION=5.2.2
BLENDER_DIR="$HOME/.local/blender-$BLENDER_VERSION-linux-x64"

SUDO=""
[ "$(id -u)" -eq 0 ] || SUDO=sudo
$SUDO apt-get update -qq
DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq ffmpeg libegl1 libgl1 libxi6 libxkbcommon0 \
    libxkbcommon-x11-0 libsm6 libxrender1 libxxf86vm1 libxfixes3 libx11-6 >/dev/null

if [ ! -x "$BLENDER_DIR/blender" ]; then
    mkdir -p "$HOME/.local"
    curl -fsSL "https://download.blender.org/release/Blender${BLENDER_VERSION%.*}/blender-$BLENDER_VERSION-linux-x64.tar.xz" \
        | tar xJ -C "$HOME/.local"
fi

[ -x "$REPO/.venv/bin/python" ] || python3 -m venv "$REPO/.venv"
"$REPO/.venv/bin/pip" install -q pillow

cd "$REPO/tools/skottie-render"
[ -d node_modules/canvaskit-wasm ] || npm install --silent --no-audit --no-fund
if [ ! -e build/skottie-render ] || grep -q skottie-render.mjs build/skottie-render 2>/dev/null; then
    mkdir -p build
    printf '#!/bin/sh\nexec node "%s/skottie-render.mjs" "$@"\n' "$REPO/tools/skottie-render" > build/skottie-render
    chmod +x build/skottie-render
fi

echo "ready. export DRIFT_BLENDER=$BLENDER_DIR/blender"
