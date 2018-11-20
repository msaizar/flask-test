#!/usr/bin/env bash

set -o errexit
set -o pipefail

flask db upgrade
/usr/local/bin/gunicorn "app.app:create_app()" --bind 0.0.0.0:5000 --timeout 1800 --chdir=/application/flask-test/
