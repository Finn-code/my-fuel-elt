CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.fuelprice (
    record_date  DATE        NOT NULL,
    series_type  TEXT        NOT NULL,
    payload      JSONB       NOT NULL,
    loaded_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (record_date, series_type)
);