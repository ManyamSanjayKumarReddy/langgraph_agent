#!/bin/sh
set -e

aerich upgrade

exec uvicorn app:app --host 0.0.0.0 --port 8003
