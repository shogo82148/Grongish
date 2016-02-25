#!/bin/bash

set -ue

echo "[$$] start"

ROOT=$(cd $(dirname $0);pwd)
CONTAINER_DIR=/var/containers/grongish-$$
mkdir -p $CONTAINER_DIR

_cleanup_dir() {
    echo "[$$] clean up"
    rm -rf $CONTAINER_DIR
    echo "[$$] finish"
}

trap _cleanup_dir EXIT

# export image
CONTAINER_ID=$(docker create grongish:latest)
echo "[$$] export container:$CONTAINER_ID into $CONTAINER_DIR"
docker export $CONTAINER_ID | tar x -C $CONTAINER_DIR
docker rm $CONTAINER_ID

# convert server-starter into gunicorn
if [[ -n "${SERVER_STARTER_PORT-}" ]]; then
    export GUNICORN_FD=$(echo $SERVER_STARTER_PORT | tr ';' ' ' | xargs -n1 | cut -d= -f2 | xargs | tr ' ' ',')
fi

# start daemon
droot run --root $CONTAINER_DIR --user app --group app /bin/bash -c "cd /Grongish && exec gunicorn -w 2 server:application" &
CHILD=$!

# Forward SIGTERM and SIGHUP to child
# http://unix.stackexchange.com/questions/146756/forward-sigterm-to-child-in-bash
_term() {
    echo "[$$] Caught SIGTERM signal!"
    kill -TERM "$CHILD" 2>/dev/null
}

_hup() {
    echo "[$$] Caught SIGHUP signal!"
    kill -TERM "$CHILD" 2>/dev/null
}

_int() {
    echo "[$$] Caught SIGINT signal!"
    kill -TERM "$CHILD" 2>/dev/null
}

trap _term SIGTERM
trap _hup SIGHUP
trap _int SIGINT

_cleanup_child() {
    echo "[$$] child $CHILD has finished. clean up"
    droot rm --root $CONTAINER_DIR
    echo "[$$] finish"
}

trap _cleanup_child EXIT

echo "[$$] child $CHILD has started."
wait "$CHILD"
