#!/bin/bash

set -ue

export LC_ALL=C

ROOT=$(cd $(dirname $0);pwd)

cd $ROOT
exec start_server --port=9002 --interval=30 --kill-old-delay=60 --pid-file=app.pid -- $ROOT/start-worker.sh
