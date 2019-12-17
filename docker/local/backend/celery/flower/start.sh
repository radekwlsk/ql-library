#!/bin/sh

set -o errexit
set -o nounset


celery flower \
    --app=ql_library.taskapp \
    --broker="${CELERY_BROKER_URL}"
