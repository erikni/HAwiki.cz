#!/bin/sh
set -eu
python3 -m pip install --target .vendor --upgrade -r requirements.txt
python3 build.py
python3 check.py
python3 check_seo.py
