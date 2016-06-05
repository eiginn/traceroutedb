#!/bin/bash

set -e -x

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PG_RESTORE=/usr/bin/pg_restore
CREATEDB=/usr/bin/createdb
DROPDB=/usr/bin/dropdb
PSQL=/usr/bin/psql
DATABASE=traceroutedb


if ! [[ -e $PG_RESTORE ]]; then
    echo missing $PG_RESTORE
    exit 4
fi

if ! [[ -e $CREATEDB ]]; then
    echo missing $CREATEDB
    exit 5
fi

if ! [[ -e $DROPDB ]]; then
    echo missing $DROPDB
    exit 6
fi

if ! [[ -e $PSQL ]]; then
    echo missing $PSQL
    exit 7
fi

if ! [[ -r "${DIR}/traceroutedb.sql" ]]; then
    echo missing "${DIR}/traceroutedb.sql"
    exit 8
fi

if ! [[ -r "${DIR}/data.sql" ]]; then
    echo missing "${DIR}/data.sql"
    exit 9
fi

echo 'Dropping existing database'
sudo -u postgres dropdb $DATABASE || true

echo creating database $DATABASE
sudo -u postgres $CREATEDB $DATABASE

echo restoring database
sudo -u postgres $PSQL -v ON_ERROR_STOP=1 -f "${DIR}/traceroutedb.sql" $DATABASE

echo restoring data
sudo -u postgres $PSQL -v ON_ERROR_STOP=1 -f "${DIR}/data.sql" $DATABASE
