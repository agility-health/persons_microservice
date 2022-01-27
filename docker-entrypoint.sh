#!/usr/bin/env bash
poetry run flask db upgrade &&
poetry run flask run --host 0.0.0.0
#poetry run python worker.py
