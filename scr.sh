#!/usr/bin/env bash

set -o errexit

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install https://github.com/aiogram/aiogram/archive/refs/heads/dev-3.x.zip