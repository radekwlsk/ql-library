#!/bin/sh

# This is just a convenient wrapper script for the in-project backend/manage.sh. It runs
# commands in docker-compose's app container. It can also contain some project tasks
# that needn't be run inside the main container, like load tests with locust.

set -o errexit
set -o nounset

cmd="$*"

help() {
    cli_name=${0##*/}
    echo "
cs-backend management CLI
Usage: $cli_name [command]
Commands:
  help
      This message
  build-local
      Build the local environment using docker-compose
  test
      Run tests
  lint
      Run linters
  sort
      Sort imports using isort
  format
      Format code using black
  generate-gql-schema
      Generate GraphQL schema files based on definitions in the code
  lock-dependencies
      Generate a lockfile containing current dependencies
  migrate
      Apply Django database migrations
  shell
      Start a Django interactive shell
  run <command>
      Run the provided command inside the local application container
"
}

build_local() {
    docker-compose build
}

case "$cmd" in
    build-local)
        build_local
    ;;
    help)
        help
    ;;
    "")
        help
    ;;
    *)
        # shellcheck disable=SC2086
        docker-compose run --rm app manage.sh ${cmd}
    ;;
esac
