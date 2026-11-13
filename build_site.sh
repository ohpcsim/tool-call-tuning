#!/bin/sh
# Build the site into _build/html from a clean state.
# Usage: ./build_site.sh   (run from anywhere)
set -eu
cd "$(dirname "$0")"
if [ ! -x .venv/bin/jupyter-book ]; then
    python3 -m venv .venv
    .venv/bin/pip install --quiet -r requirements.txt
fi
rm -rf _build
PATH="$PWD/.venv/bin:$PATH" jupyter-book build --site --html --execute --strict
