"""A fake in-memory database: a dict of table name -> list of rows."""

DB: dict[str, list[dict[str, str]]] = {}


def insert_rows(table: str, rows: list[dict[str, str]]) -> int:
    DB.setdefault(table, []).extend(rows)
    return len(rows)


def get_rows(table: str) -> list[dict[str, str]]:
    return DB.get(table, [])


def reset() -> None:
    DB.clear()
