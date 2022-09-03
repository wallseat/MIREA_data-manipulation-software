#!/bin/bash

set -eou pipefail


DOCKER_ID=$(docker ps -f "name=postgresql-edu" | tail -n 1 | awk '{print $1}')
if [ -z "$DOCKER_ID" ]; then
    echo "No docker container found"
    exit 1
fi

if ! [[ -e "../shared/demo-small-20170815.sql" ]]; then
    wget https://edu.postgrespro.ru/demo-small.zip -O ../shared/demo-small.zip
    unzip -q -o ../shared/demo-small.zip -d ../shared
    rm -f ../shared.zip
fi

docker exec -it $DOCKER_ID  /bin/bash -c "psql -q -U postgres -f /shared/demo-small-20170815.sql"