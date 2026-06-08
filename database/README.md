# Database Layer

This app uses SQLite for a small, portable database that can be rebuilt from the
provided CSV files.

## Files

- `schema.sql`: Creates normalized patient, diagnosis, and gene tables.
- `seed_database.py`: Rebuilds `app.db` from the CSV files in `data/`.
- `app.db`: Generated SQLite database used by the Flask API.

## Schema

- `patients`: One row per patient from `fake_patient_details.csv`.
- `diagnoses`: Unique cancer diagnosis lookup values.
- `patient_diagnoses`: Links patients to diagnoses.
- `genes`: Unique gene lookup values.
- `patient_genes`: Links patients to zero or more genes.
- `patient_summaries`: Read view for list screens and API responses.

## Rebuild

```bash
python3 database/seed_database.py
```

## Validate

```bash
python3 database/validate_database.py
```

The validation script checks expected row counts, relationship integrity, common
filter queries, and the `patient_summaries` view that the Flask API will use.

## Query Direction

The patient list endpoint can query `patient_summaries` for display. Filters by
diagnosis and gene should still use joins against the normalized tables so a
patient can match one requested gene without losing their other genes in the
display response.
