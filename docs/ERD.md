# Entity Relationship Diagram

```mermaid
erDiagram
    PATIENTS ||--o{ PATIENT_DIAGNOSES : has
    DIAGNOSES ||--o{ PATIENT_DIAGNOSES : classifies
    PATIENTS ||--o{ PATIENT_GENES : has
    GENES ||--o{ PATIENT_GENES : identifies

    PATIENTS {
        text patient_id PK
        text first_name
        text last_name
        text gender
        text street_address
        text city
        text state
        text zip_code
        text phone
    }

    DIAGNOSES {
        integer diagnosis_id PK
        text name UK
    }

    PATIENT_DIAGNOSES {
        text patient_id PK, FK
        integer diagnosis_id PK, FK
    }

    GENES {
        integer gene_id PK
        text symbol UK
    }

    PATIENT_GENES {
        text patient_id PK, FK
        integer gene_id PK, FK
    }
```

## Notes

- `patients` stores one row per patient from `fake_patient_details.csv`.
- `diagnoses` and `genes` are lookup tables so repeated values are stored once.
- `patient_diagnoses` links patients to their cancer diagnosis.
- `patient_genes` supports patients having zero, one, or multiple genes.
- `patient_summaries` is a read-only SQL view used by the patient list API.
