#!/bin/bash

set -ue

if [[ -n "${SERVER_STARTER_PORT-}" ]]; then
    export GUNICORN_FD=$(echo $SERVER_STARTER_PORT | tr ';' ' ' | xargs -n1 | cut -d= -f2 | xargs | tr ' ' ',')
fi

exec gunicorn server:application
