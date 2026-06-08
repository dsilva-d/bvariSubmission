from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request

from . import db


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=str(db.default_database_path()),
        JSON_SORT_KEYS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        return response

    @app.get("/api/health")
    def health():
        database_path = Path(app.config["DATABASE"])
        return jsonify(
            {
                "status": "ok",
                "database_exists": database_path.exists(),
            }
        )

    @app.get("/api/filters")
    def filters():
        connection = db.get_db()

        states = connection.execute(
            "SELECT DISTINCT state FROM patients ORDER BY state"
        ).fetchall()
        diagnoses = connection.execute(
            "SELECT name FROM diagnoses ORDER BY name"
        ).fetchall()
        genes = connection.execute("SELECT symbol FROM genes ORDER BY symbol").fetchall()

        return jsonify(
            {
                "states": [row["state"] for row in states],
                "diagnoses": [row["name"] for row in diagnoses],
                "genes": [row["symbol"] for row in genes],
            }
        )

    @app.get("/api/patients")
    def patients():
        connection = db.get_db()
        where_clauses, params = build_patient_filters(request.args)

        sql = """
            SELECT
                patient_id,
                first_name,
                last_name,
                gender,
                city,
                state,
                diagnosis,
                genes
            FROM patient_summaries ps
        """

        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

        sql += " ORDER BY last_name, first_name, patient_id"

        rows = connection.execute(sql, params).fetchall()
        return jsonify([format_patient_summary(row) for row in rows])

    @app.get("/api/patients/<patient_id>")
    def patient(patient_id: str):
        connection = db.get_db()
        row = connection.execute(
            """
            SELECT
                patient_id,
                first_name,
                last_name,
                gender,
                street_address,
                city,
                state,
                zip_code,
                phone
            FROM patients
            WHERE patient_id = ?
            """,
            (patient_id,),
        ).fetchone()

        if row is None:
            return jsonify({"error": "Patient not found"}), 404

        diagnosis_rows = connection.execute(
            """
            SELECT d.name
            FROM patient_diagnoses pd
            JOIN diagnoses d ON d.diagnosis_id = pd.diagnosis_id
            WHERE pd.patient_id = ?
            ORDER BY d.name
            """,
            (patient_id,),
        ).fetchall()

        gene_rows = connection.execute(
            """
            SELECT g.symbol
            FROM patient_genes pg
            JOIN genes g ON g.gene_id = pg.gene_id
            WHERE pg.patient_id = ?
            ORDER BY g.symbol
            """,
            (patient_id,),
        ).fetchall()

        payload = db.dict_from_row(row)
        payload["diagnoses"] = [diagnosis["name"] for diagnosis in diagnosis_rows]
        payload["genes"] = [gene["symbol"] for gene in gene_rows]

        return jsonify(payload)

    return app


def build_patient_filters(args) -> tuple[list[str], list[str]]:
    where_clauses: list[str] = []
    params: list[str] = []

    text_filters = {
        "first_name": "ps.first_name",
        "last_name": "ps.last_name",
    }

    for query_name, column_name in text_filters.items():
        value = args.get(query_name, "").strip()
        if value:
            where_clauses.append(f"LOWER({column_name}) LIKE LOWER(?)")
            params.append(f"%{value}%")

    state = args.get("state", "").strip()
    if state:
        where_clauses.append("ps.state = ?")
        params.append(state.upper())

    diagnosis = args.get("diagnosis", "").strip()
    if diagnosis:
        where_clauses.append("ps.diagnosis = ?")
        params.append(diagnosis)

    gene = args.get("gene", "").strip()
    if gene:
        where_clauses.append(
            """
            EXISTS (
                SELECT 1
                FROM patient_genes pg
                JOIN genes g ON g.gene_id = pg.gene_id
                WHERE pg.patient_id = ps.patient_id
                    AND g.symbol = ?
            )
            """
        )
        params.append(gene.upper())

    return where_clauses, params


def format_patient_summary(row) -> dict[str, object]:
    payload = db.dict_from_row(row)
    genes = payload.get("genes")
    payload["genes"] = genes.split(",") if isinstance(genes, str) and genes else []
    return payload


app = create_app()
