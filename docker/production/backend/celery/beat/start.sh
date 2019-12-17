#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

celery -A ql_library.taskapp beat -l INFO
