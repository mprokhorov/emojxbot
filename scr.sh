#!/usr/bin/env bash

set -o errexit

/opt/render/project/scr/.venv/bin/python -m pip install --upgrade pip

pip install https://github.com/aiogram/aiogram/archive/refs/heads/dev-3.x.zip