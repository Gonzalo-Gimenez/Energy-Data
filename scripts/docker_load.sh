#!/bin/bash
set -euo pipefail
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  -c "TRUNCATE fuel_prices;"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  -c "COPY fuel_prices FROM '/data/fuel_prices.csv' CSV HEADER;"
