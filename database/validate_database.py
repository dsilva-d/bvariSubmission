from __future__ import annotations

import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "database" / "app.db"


EXPECTED_COUNTS = {
    "patients": 200,
    "diagnoses": 10,
    "patient_diagnoses": 200,
    "genes": 5,
    "patient_genes": 49,
    "patient_summaries": 200,
}


def fetch_count(conn: sqlite3.Connection, table_or_view: str) -> int:
    row = conn.execute(f"SELECT count(*) AS row_count FROM {table_or_view}").fetchone()
    return int(row["row_count"])


def assert_no_rows(conn: sqlite3.Connection, query: str, label: str) -> None:
    count = int(conn.execute(query).fetchone()["row_count"])
    if count:
        raise AssertionError(f"{label}: expected 0, found {count}")


def validate() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    for table_or_view, expected in EXPECTED_COUNTS.items():
        actual = fetch_count(conn, table_or_view)
        if actual != expected:
            raise AssertionError(
                f"{table_or_view}: expected {expected} rows, found {actual}"
            )
        print(f"OK {table_or_view}: {actual} rows")

    assert_no_rows(
        conn,
        """
        SELECT count(*) AS row_count
        FROM patient_diagnoses pd
        LEFT JOIN patients p ON p.patient_id = pd.patient_id
        WHERE p.patient_id IS NULL
        """,
        "diagnoses with missing patients",
    )
    print("OK every diagnosis belongs to a patient")

    assert_no_rows(
        conn,
        """
        SELECT count(*) AS row_count
        FROM patient_genes pg
        LEFT JOIN patients p ON p.patient_id = pg.patient_id
        WHERE p.patient_id IS NULL
        """,
        "genes with missing patients",
    )
    print("OK every gene belongs to a patient")

    filters = {
        "first_name": ("p.first_name = ?", "Celeste"),
        "last_name": ("p.last_name = ?", "Fowkes"),
        "state": ("p.state = ?", "WA"),
        "diagnosis": ("d.name = ?", "heart"),
        "gene": ("g.symbol = ?", "BCD"),
    }

    for label, (predicate, value) in filters.items():
        row = conn.execute(
            f"""
            SELECT count(DISTINCT p.patient_id) AS row_count
            FROM patients p
            LEFT JOIN patient_diagnoses pd ON pd.patient_id = p.patient_id
            LEFT JOIN diagnoses d ON d.diagnosis_id = pd.diagnosis_id
            LEFT JOIN patient_genes pg ON pg.patient_id = p.patient_id
            LEFT JOIN genes g ON g.gene_id = pg.gene_id
            WHERE {predicate}
            """,
            (value,),
        ).fetchone()
        count = int(row["row_count"])
        if count < 1:
            raise AssertionError(f"{label} filter returned no rows for {value}")
        print(f"OK {label} filter returns {count} patient(s)")

    sample = conn.execute(
        """
        SELECT *
        FROM patient_summaries
        WHERE patient_id = ?
        """,
        ("00-322-1846",),
    ).fetchone()
    if not sample:
        raise AssertionError("sample patient summary was not found")

    print("OK patient_summaries exposes list-page data")
    conn.close()


if __name__ == "__main__":
    validate()
    print("Database validation passed")
