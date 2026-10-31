"""Extract fuel prices from data.gov.my and load them into raw.fuelprice."""

import logging
import os

import psycopg
import requests
from dotenv import load_dotenv
from psycopg.types.json import Jsonb

API_URL = "https://api.data.gov.my/data-catalogue/"
DATASET_ID = "fuelprice"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def fetch_records() -> list[dict]:
    """Call the API and return a list of records. Fails loudly on anything unexpected."""
    response = requests.get(API_URL, params={"id": DATASET_ID}, timeout=30)
    response.raise_for_status()  # crash on 4xx/5xx instead of silently continuing

    data = response.json()
    if not isinstance(data, list):
        raise ValueError(f"Expected a list from the API, got {type(data).__name__}")

    log.info("Fetched %d records", len(data))
    return data

def to_rows(records: list[dict]) -> list[tuple]:
    """Turn API records into (record_date, series_type, payload) tuples for the database."""
    return [(r["date"], r["series_type"], Jsonb(r)) for r in records]

def load_records(records: list[dict], conn: psycopg.Connection) -> None:
    """Insert records. If a (date, series_type) already exists, update it instead."""
    sql = """
        INSERT INTO raw.fuelprice (record_date, series_type, payload)
        VALUES (%s, %s, %s)
        ON CONFLICT (record_date, series_type)
        DO UPDATE SET payload = EXCLUDED.payload, loaded_at = now()
    """
    rows = to_rows(records)

    with conn.cursor() as cur:
        cur.executemany(sql, rows)
    conn.commit()
    log.info("Loaded %d rows into raw.fuelprice", len(rows))


def main() -> None:
    load_dotenv()
    conninfo = (
        f"host=localhost port=5432 "
        f"dbname={os.environ['POSTGRES_DB']} "
        f"user={os.environ['POSTGRES_USER']} "
        f"password={os.environ['POSTGRES_PASSWORD']}"
    )

    records = fetch_records()
    with psycopg.connect(conninfo) as conn:
        load_records(records, conn)


if __name__ == "__main__":
    main()