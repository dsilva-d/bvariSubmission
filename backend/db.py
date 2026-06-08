from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import current_app, g


def dict_from_row(row: sqlite3.Row) -> dict[str, object]:
    return {key: row[key] for key in row.keys()}


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        connection = sqlite3.connect(current_app.config["DATABASE"])
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection

    return g.db


def close_db(error: BaseException | None = None) -> None:
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app) -> None:
    app.teardown_appcontext(close_db)


def default_database_path() -> Path:
    return Path(__file__).resolve().parents[1] / "database" / "app.db"
