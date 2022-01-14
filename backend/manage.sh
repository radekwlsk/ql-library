#!/bin/sh

set -o errexit
set -o nounset


cmd="$1"
shift 1
args="$*"

PYTEST="pytest --ds ${DJANGO_SETTINGS_MODULE_TEST}"

# default test flags
RUNTEST="$PYTEST \
    --durations=10 \
    --cov"

lint() {
    black --check . || echo "Try running ./manage.sh format"
    isort --check-only . || echo "Try running ./manage.sh sort"
    pylama
}

migrate() {
    python manage.py migrate --noinput
}

shell() {
    python manage.py shell
}

generate_gql_schema() {
    DJANGO_DEBUG=0 python manage.py graphql_schema --out schema.json
    DJANGO_DEBUG=0 python manage.py graphql_schema --out schema.graphql
}

case "$cmd" in
    test)
        ${RUNTEST}
    ;;
    lint)
        lint
    ;;
    sort)
        isort --atomic --skip /app/shared/media/ .
    ;;
    format)
        black --exclude /app/shared/media/ .
    ;;
    generate-gql-schema)
        generate_gql_schema
    ;;
    lock-dependencies)
        # If we don't have a Pipfile.lock in the app directory, that means this is the
        # first build and we should use the one generated during the build
        if [ ! -f Pipfile.lock ]; then
            cp "${BUILD_PIPFILE_LOCK}" Pipfile.lock
        else
            pipenv lock
        fi
    ;;
    migrate)
        migrate
    ;;
    shell)
        shell
    ;;
    run)
        $args  # run the command passed in as the argument
    ;;
    *)
        echo "Unknown command: $cmd $args"
        exit 1
esac
