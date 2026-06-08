# Patient Study Finder

Small Flask, SQLite, and React app for screening cancer patients by name, state,
diagnosis, and gene.

## Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 database/seed_database.py
flask --app backend.app run --debug
```

Backend URL: `http://127.0.0.1:5000`

## Frontend

First-time setup:

```bash
cd frontend
npm install
```

Run:

```bash
npm run dev
```

Frontend URL: `http://127.0.0.1:5173`

If `npm run dev` reports `vite: command not found`, run `npm install` inside
the `frontend/` directory and try again.

## Stop Servers

Press `Ctrl + C` in each terminal where Flask or Vite is running.

## Checks

```bash
python3 database/validate_database.py
.venv/bin/python backend/smoke_test_api.py
cd frontend
npm run build
```

## Design Notes

- Database ERD: [docs/ERD.md](docs/ERD.md)

## Submission File

The exercise asks for a zip file renamed with a `.txt` extension. Create it from
the project root:

```bash
python3 scripts/create_submission.py --first-name YourFirstName --last-name YourLastName
```

The file will be created in `submission/`:

```text
Software_Developer_Exercise_2026-YourLastNameYourFirstName.txt
```

The submission includes source files, CSVs, `database/app.db`, lock files, and
run documentation. It excludes local dependency folders such as `.venv` and
`frontend/node_modules`, which can be recreated from `requirements.txt` and
`frontend/package-lock.json`.
