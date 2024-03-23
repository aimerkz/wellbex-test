#!/bin/bash -x

python3 manage.py migrate --noinput || exit 1

python3 manage.py load_locations locations/uszips.csv && \
python3 manage.py create_cars 20 && \
python3 manage.py update_locations_task create

exec "$@"
