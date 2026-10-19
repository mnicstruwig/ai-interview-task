import csv
import io

from fastapi import FastAPI, HTTPException, UploadFile

from app import db

app = FastAPI(title="Toy Data Warehouse")


@app.post("/ingest/{table}")
async def ingest_csv(table: str, file: UploadFile):
    """Ingest a CSV file into the given table."""
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")

    content = (await file.read()).decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(content)))
    if not rows:
        raise HTTPException(status_code=400, detail="CSV contains no rows")

    inserted = db.insert_rows(table, rows)
    return {"table": table, "rows_inserted": inserted, "total_rows": len(db.get_rows(table))}


@app.get("/tables/{table}")
def get_table(table: str):
    """Retrieve all rows in the given table."""
    if table not in db.DB:
        raise HTTPException(status_code=404, detail=f"Table '{table}' not found")

    rows = db.get_rows(table)
    return {"table": table, "row_count": len(rows), "rows": rows}
