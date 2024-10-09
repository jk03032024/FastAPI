#!/bin/bash

echo "this is working"

set -e

echo "Starting postgres container"
sudo docker compose run postgres -d || true

echo "Applying DB changes using liquibase"
sudo docker compose run liquibase

