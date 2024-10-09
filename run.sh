#!/usr/bin/bash
set -e

if [ "$1" == "db" ]
then
    echo "Starting postgres container"
    docker compose run postgres -d || true

    echo "Applying DB changes using liquibase"
    docker compose run liquibase

elif [ "$1" == "tests" ]
then
    echo "Starting postgres container"
    docker compose run postgres -d || true

    echo "Applying Db changes using liquibase"
    docker compose run liquibase

    echo "running tests and generating tests coverage"
    docker compose run tests
    #cd tests
    #pytest

    #echo "Generating tests coverage"
    #coverage report

    if [ "$2" == "NO_DB_SHUTDOWN" ]
    then
        echo "Keeping DB up"
    else
        docker compose down
    fi

elif [ "$1" == "apis" ]
then
    echo "Starting postgres container"
    docker compose run postgres -d || true

    # echo "Applying Db changes using liquibase"
    # docker compose run liquibase
    
    echo "Building and starting APIs"
    docker compose run apis
     docker compose down
else
    echo "Incorrect flags"
fi