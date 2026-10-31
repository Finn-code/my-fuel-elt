"""Unit tests for the fuel price extract script. No internet or database needed."""

from unittest.mock import Mock, patch

import pytest
import requests

from extract import fuelprice

SAMPLE_RECORD = {
    "date": "2026-10-22",
    "series_type": "level",
    "ron95": 4.32,
    "ron95_budi95": 1.99,
}


def fake_response(json_data, status_code=200):
    """Build a fake requests.Response that returns json_data."""
    response = Mock()
    response.json.return_value = json_data
    if status_code >= 400:
        response.raise_for_status.side_effect = requests.HTTPError(f"{status_code} error")
    return response


# ---------- fetch_records ----------

@patch("extract.fuelprice.requests.get")
def test_fetch_returns_records(mock_get):
    mock_get.return_value = fake_response([SAMPLE_RECORD])

    assert fuelprice.fetch_records() == [SAMPLE_RECORD]


@patch("extract.fuelprice.requests.get")
def test_fetch_uses_url_with_trailing_slash(mock_get):
    # Regression test: without the trailing slash, the API returns a 301 redirect.
    mock_get.return_value = fake_response([SAMPLE_RECORD])

    fuelprice.fetch_records()

    called_url = mock_get.call_args.args[0]
    assert called_url == "https://api.data.gov.my/data-catalogue/"
    assert mock_get.call_args.kwargs["params"] == {"id": "fuelprice"}


@patch("extract.fuelprice.requests.get")
def test_fetch_raises_on_http_error(mock_get):
    mock_get.return_value = fake_response(None, status_code=500)

    with pytest.raises(requests.HTTPError):
        fuelprice.fetch_records()


@patch("extract.fuelprice.requests.get")
def test_fetch_rejects_non_list_response(mock_get):
    # e.g. the API returns an error object instead of a list of records
    mock_get.return_value = fake_response({"error": "something went wrong"})

    with pytest.raises(ValueError):
        fuelprice.fetch_records()


# ---------- to_rows ----------

def test_to_rows_builds_key_and_payload():
    rows = fuelprice.to_rows([SAMPLE_RECORD])

    record_date, series_type, payload = rows[0]
    assert record_date == "2026-10-22"
    assert series_type == "level"
    assert payload.obj == SAMPLE_RECORD  # full record kept untouched


def test_to_rows_fails_if_key_field_missing():
    broken = {"series_type": "level", "ron95": 4.32}  # no "date"

    with pytest.raises(KeyError):
        fuelprice.to_rows([broken])