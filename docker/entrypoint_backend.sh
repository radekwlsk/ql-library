#!/bin/sh

set -o errexit
set -o pipefail
# todo: turn on after #1295
# set -o nounset


cmd="$@"

# We only want to run pytest with an explicitly set django settings module
PYTEST="pytest --ds ${DJANGO_SETTINGS_MODULE_TEST}"
migrate() {
    python manage.py migrate --noinput
}

collectstatic() {
    python manage.py collectstatic --clear --no-input
}
postgres_ready() {
    python << END
import sys
import psycopg2

try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}")
except psycopg2.OperationalError:
    sys.exit(-1)

sys.exit(0)
END
}


counter=0
until postgres_ready; do
  >&2 echo 'PostgreSQL is unavailable (sleeping)...'
  sleep 1
  if [ $counter -gt "60" ]; then
    echo "Can't connect to PostgreSQL. Exiting."
    exit 1
  fi
  counter=$(expr $counter + 1)
done

>&2 echo 'PostgreSQL is up - continuing...'


case "$cmd" in
    runtest)
        $PYTEST \
            --cov ql_library --cov-report xml \
            --pylama \
            --verbose
    ;;
    lint)
        pylama
    ;;
    sort)
        isort -rc --atomic .
    ;;
    format)
        black .
    ;;
    gqlschema)
        python manage.py graphql_schema --out schema.json
        python manage.py graphql_schema --out schema.graphql
    ;;
    runcitest)
        pipenv install --dev
        pipenv run $PYTEST \
            --cov test --cov-report xml \
            --verbose \
            --pylama
        pipenv --rm
    ;;
    lock-dependencies)
        # If we don't have a Pipfile.lock in the app directory, that means this is the
        # first build and we should use the one generated during the build
        if [ ! -f Pipfile.lock ]; then
            cp $BUILD_PIPFILE_LOCK Pipfile.lock
        else
          pipenv lock && pipenv --rm
        fi
    ;;
    
    migrate)
        migrate
    ;;
    collectstatic)
        collectstatic
    ;;
    jupyter)
        python manage.py shell_plus --notebook
    ;;
    builddoc)
        sphinx-build -a -b html -d /docs/build/doctrees /docs/source /docs/build/html
    ;;
    lint)
        pylama
    ;;
    *)
        $cmd  # usage start.sh or gunicorn.sh
    ;;
esac
