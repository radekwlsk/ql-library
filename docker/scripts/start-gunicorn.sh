#!/bin/sh
# https://gunicorn-docs.readthedocs.io/en/stable/settings.html

set -o errexit
set -o nounset

gunicorn config.wsgi:application \
        --bind ${GUNICORN_HOST:-0.0.0.0}:${GUNICORN_PORT:-8000} \
        --timeout ${GUNICORN_TIMEOUT:-300} \
        --max-requests ${GUNICORN_MAX_REQUESTS:-5000} \
        --workers ${GUNICORN_WORKERS:-2} \
        --threads ${GUNICORN_THREADS:-4} \
        --worker-class ${GUNICORN_WORKER_CLASS:-sync} \
        --worker-tmp-dir /dev/shm \
        --name ql_library \
        --access-logfile ${GUNICORN_ACCESS_LOGFILE:--} \
        --error-logfile ${GUNICORN_ERROR_LOGFILE:--} \
        --chdir /app
