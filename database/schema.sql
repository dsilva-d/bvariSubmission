PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS patient_genes;
DROP TABLE IF EXISTS patient_diagnoses;
DROP TABLE IF EXISTS genes;
DROP TABLE IF EXISTS diagnoses;
DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    patient_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    street_address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE diagnoses (
    diagnosis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE patient_diagnoses (
    patient_id TEXT NOT NULL,
    diagnosis_id INTEGER NOT NULL,
    PRIMARY KEY (patient_id, diagnosis_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (diagnosis_id) REFERENCES diagnoses(diagnosis_id) ON DELETE RESTRICT
);

CREATE TABLE genes (
    gene_id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL UNIQUE
);

CREATE TABLE patient_genes (
    patient_id TEXT NOT NULL,
    gene_id INTEGER NOT NULL,
    PRIMARY KEY (patient_id, gene_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (gene_id) REFERENCES genes(gene_id) ON DELETE RESTRICT
);

CREATE INDEX idx_patients_first_name ON patients(first_name);
CREATE INDEX idx_patients_last_name ON patients(last_name);
CREATE INDEX idx_patients_state ON patients(state);
CREATE INDEX idx_diagnoses_name ON diagnoses(name);
CREATE INDEX idx_genes_symbol ON genes(symbol);
CREATE INDEX idx_patient_diagnoses_diagnosis ON patient_diagnoses(diagnosis_id);
CREATE INDEX idx_patient_genes_gene ON patient_genes(gene_id);

CREATE VIEW patient_summaries AS
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    p.gender,
    p.city,
    p.state,
    d.name AS diagnosis,
    group_concat(g.symbol, ',') AS genes
FROM patients p
LEFT JOIN patient_diagnoses pd
    ON pd.patient_id = p.patient_id
LEFT JOIN diagnoses d
    ON d.diagnosis_id = pd.diagnosis_id
LEFT JOIN patient_genes pg
    ON pg.patient_id = p.patient_id
LEFT JOIN genes g
    ON g.gene_id = pg.gene_id
GROUP BY
    p.patient_id,
    p.first_name,
    p.last_name,
    p.gender,
    p.city,
    p.state,
    d.name;
