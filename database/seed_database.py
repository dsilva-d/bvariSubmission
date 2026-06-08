from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = ROOT_DIR / "database" / "app.db"
SCHEMA_PATH = ROOT_DIR / "database" / "schema.sql"


def read_csv(filename: str) -> list[dict[str, str]]:
    with (DATA_DIR / filename).open(newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def get_or_create_id(
    conn: sqlite3.Connection,
    table: str,
    id_column: str,
    value_column: str,
    value: str,
) -> int:
    row = conn.execute(
        f"SELECT {id_column} FROM {table} WHERE {value_column} = ?",
        (value,),
    ).fetchone()
    if row:
        return int(row[id_column])

    cursor = conn.execute(
        f"INSERT INTO {table} ({value_column}) VALUES (?)",
        (value,),
    )
    return int(cursor.lastrowid)


def seed() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    with conn:
        conn.executescript(SCHEMA_PATH.read_text())

        patient_rows = read_csv("fake_patient_details.csv")
        conn.executemany(
            """
            INSERT INTO patients (
                patient_id,
                first_name,
                last_name,
                gender,
                street_address,
                city,
                state,
                zip_code,
                phone
            )
            VALUES (
                :patient_id,
                :first_name,
                :last_name,
                :gender,
                :street_address,
                :city,
                :state,
                :zip_code,
                :phone
            )
            """,
            patient_rows,
        )

        for row in read_csv("fake_patient_diagnosis.csv"):
            diagnosis_id = get_or_create_id(
                conn,
                table="diagnoses",
                id_column="diagnosis_id",
                value_column="name",
                value=row["diagnosis"],
            )
            conn.execute(
                """
                INSERT INTO patient_diagnoses (patient_id, diagnosis_id)
                VALUES (?, ?)
                """,
                (row["patient_id"], diagnosis_id),
            )

        for row in read_csv("fake_patient_genes.csv"):
            gene_id = get_or_create_id(
                conn,
                table="genes",
                id_column="gene_id",
                value_column="symbol",
                value=row["gene"],
            )
            conn.execute(
                """
                INSERT OR IGNORE INTO patient_genes (patient_id, gene_id)
                VALUES (?, ?)
                """,
                (row["patient_id"], gene_id),
            )

    conn.close()


if __name__ == "__main__":
    seed()
    print(f"Seeded SQLite database at {DB_PATH}")
