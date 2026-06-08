from __future__ import annotations

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from backend.app import create_app


def assert_status(response, expected_status: int) -> None:
    if response.status_code != expected_status:
        raise AssertionError(
            f"Expected {expected_status}, received {response.status_code}: "
            f"{response.get_data(as_text=True)}"
        )


def main() -> None:
    app = create_app()

    with app.test_client() as client:
        health = client.get("/api/health")
        assert_status(health, 200)
        assert health.json["status"] == "ok"
        assert health.json["database_exists"] is True
        print("OK /api/health")

        filters = client.get("/api/filters")
        assert_status(filters, 200)
        assert len(filters.json["states"]) > 0
        assert len(filters.json["diagnoses"]) == 10
        assert len(filters.json["genes"]) == 5
        print("OK /api/filters")

        patients = client.get("/api/patients")
        assert_status(patients, 200)
        assert len(patients.json) == 200
        assert {"patient_id", "first_name", "last_name", "diagnosis", "genes"}.issubset(
            patients.json[0].keys()
        )
        print("OK /api/patients")

        filtered = client.get("/api/patients?state=WA&diagnosis=heart&gene=BCD")
        assert_status(filtered, 200)
        assert len(filtered.json) >= 1
        assert all(patient["state"] == "WA" for patient in filtered.json)
        assert all(patient["diagnosis"] == "heart" for patient in filtered.json)
        assert all("BCD" in patient["genes"] for patient in filtered.json)
        print("OK /api/patients filters")

        patient_id = patients.json[0]["patient_id"]
        detail = client.get(f"/api/patients/{patient_id}")
        assert_status(detail, 200)
        assert detail.json["patient_id"] == patient_id
        assert "street_address" in detail.json
        assert "diagnoses" in detail.json
        assert "genes" in detail.json
        print("OK /api/patients/<patient_id>")

        missing = client.get("/api/patients/not-a-real-id")
        assert_status(missing, 404)
        print("OK missing patient returns 404")

    print("API smoke tests passed")


if __name__ == "__main__":
    main()
