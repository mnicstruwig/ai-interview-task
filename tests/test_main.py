from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app

client = TestClient(app)
SAMPLE_CSV = Path(__file__).parent.parent / "data" / "businesses.csv"


@pytest.fixture(autouse=True)
def clean_db():
    db.reset()
    yield
    db.reset()


def test_ingest_sample_csv():
    with SAMPLE_CSV.open("rb") as f:
        response = client.post("/ingest/businesses", files={"file": ("businesses.csv", f, "text/csv")})

    assert response.status_code == 200
    assert response.json()["rows_inserted"] == 10

    table = client.get("/tables/businesses").json()
    assert table["row_count"] == 10
    assert table["rows"][0]["name"] == "Acme Widgets"


def test_ingest_appends_to_existing_table():
    csv_bytes = b"id,name\n1,Foo\n2,Bar\n"
    client.post("/ingest/things", files={"file": ("a.csv", csv_bytes, "text/csv")})
    response = client.post("/ingest/things", files={"file": ("b.csv", csv_bytes, "text/csv")})

    assert response.json()["total_rows"] == 4


def test_rejects_non_csv_file():
    response = client.post("/ingest/things", files={"file": ("notes.txt", b"hello", "text/plain")})

    assert response.status_code == 400
    assert db.get_rows("things") == []
