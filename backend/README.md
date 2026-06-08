# Flask API

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 database/seed_database.py
flask --app backend.app run --debug
```

The API runs at `http://127.0.0.1:5000`.

## Smoke Test

```bash
python3 backend/smoke_test_api.py
```

## Endpoints

- `GET /api/health`
- `GET /api/filters`
- `GET /api/patients`
- `GET /api/patients/<patient_id>`

## Patient Filters

`GET /api/patients` accepts these optional query parameters:

- `first_name`
- `last_name`
- `state`
- `diagnosis`
- `gene`

Example:

```bash
curl "http://127.0.0.1:5000/api/patients?state=WA&diagnosis=heart&gene=BCD"
```
