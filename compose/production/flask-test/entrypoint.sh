#!/usr/bin/env bash

set -o errexit
set -o pipefail

# todo: turn on after #1295
# set -o nounset


cmd="$@"

# the official postgres image uses 'postgres' as default user if not set explictly.
if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi

export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB_NAME

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_DB_NAME", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="$POSTGRES_HOST")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."
exec $cmd
