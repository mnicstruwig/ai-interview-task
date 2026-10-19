# Toy Data Warehouse

A simple FastAPI "data warehouse" that ingests CSV files.

## Setup

```bash
uv sync
```

## Run

```bash
./start.sh
```

Interactive docs: http://127.0.0.1:8000/docs

## Ingest a CSV

```bash
curl -F "file=@data/businesses.csv" http://127.0.0.1:8000/ingest/businesses
# {"table":"businesses","rows_inserted":10,"total_rows":10}
```

Each upload appends rows to the named table. Data lives only in memory and is
lost when the server restarts.

## Retrieve a table

```bash
curl http://127.0.0.1:8000/tables/businesses
# {"table":"businesses","row_count":10,"rows":[{"id":"1","name":"Acme Widgets",...}, ...]}
```

Returns 404 if the table doesn't exist.

## Test

```bash
./run-tests.sh            # extra args are passed to pytest, e.g. ./run-tests.sh -v
```

## Layout

```
app/
  main.py     # FastAPI app POST /ingest/{table} and GET /tables/{table}
  db.py       # the fake in-memory DB (a dict of table -> rows)
data/
  businesses.csv   # toy dataset of 10 businesses
tests/
  test_main.py     # 3 tests
```
