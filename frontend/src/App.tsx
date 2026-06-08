import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  ClipboardList,
  Loader2,
  MapPin,
  RotateCcw,
  Search,
  UserRound,
  UsersRound
} from "lucide-react";
import {
  fetchFilterOptions,
  fetchPatient,
  fetchPatients,
  type FilterOptions,
  type PatientDetail,
  type PatientFilters,
  type PatientSummary
} from "./api";

const emptyFilters: PatientFilters = {
  first_name: "",
  last_name: "",
  state: "",
  diagnosis: "",
  gene: ""
};

export function App() {
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    states: [],
    diagnoses: [],
    genes: []
  });
  const [filters, setFilters] = useState<PatientFilters>(emptyFilters);
  const [patients, setPatients] = useState<PatientSummary[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>("");
  const [selectedPatient, setSelectedPatient] = useState<PatientDetail | null>(null);
  const [isLoadingPatients, setIsLoadingPatients] = useState(true);
  const [isLoadingPatient, setIsLoadingPatient] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchFilterOptions()
      .then(setFilterOptions)
      .catch(() => setError("Unable to load filter options from the API."));
  }, []);

  useEffect(() => {
    let isCurrent = true;
    setIsLoadingPatients(true);
    setError("");

    fetchPatients(filters)
      .then((data) => {
        if (!isCurrent) return;
        setPatients(data);
        setSelectedPatientId((currentPatientId) => {
          if (data.some((patient) => patient.patient_id === currentPatientId)) {
            return currentPatientId;
          }

          return data.length ? data[0].patient_id : "";
        });
        if (!data.length) {
          setSelectedPatient(null);
        }
      })
      .catch(() => {
        if (isCurrent) {
          setError("Unable to load patients. Confirm the Flask API is running.");
        }
      })
      .finally(() => {
        if (isCurrent) {
          setIsLoadingPatients(false);
        }
      });

    return () => {
      isCurrent = false;
    };
  }, [filters]);

  useEffect(() => {
    if (!selectedPatientId) return;

    let isCurrent = true;
    setIsLoadingPatient(true);

    fetchPatient(selectedPatientId)
      .then((data) => {
        if (isCurrent) {
          setSelectedPatient(data);
        }
      })
      .catch(() => {
        if (isCurrent) {
          setSelectedPatient(null);
          setError("Unable to load the selected patient.");
        }
      })
      .finally(() => {
        if (isCurrent) {
          setIsLoadingPatient(false);
        }
      });

    return () => {
      isCurrent = false;
    };
  }, [selectedPatientId]);

  const activeFilterCount = useMemo(
    () => Object.values(filters).filter((value) => value.trim()).length,
    [filters]
  );

  function updateFilter(name: keyof PatientFilters, value: string) {
    setFilters((current) => ({ ...current, [name]: value }));
  }

  function resetFilters() {
    setFilters(emptyFilters);
  }

  return (
    <main className="app-shell">
      <section className="app-header">
        <div>
          <p className="eyebrow">Clinical study screening</p>
          <h1>Patient Study Finder</h1>
        </div>
        <div className="status-strip" aria-label="Patient result counts">
          <div>
            <UsersRound size={18} aria-hidden="true" />
            <span>{patients.length}</span>
            <small>matches</small>
          </div>
          <div>
            <Activity size={18} aria-hidden="true" />
            <span>{activeFilterCount}</span>
            <small>filters</small>
          </div>
        </div>
      </section>

      <section className="filter-bar" aria-label="Patient filters">
        <label htmlFor="first-name-filter">
          <span>First name</span>
          <input
            id="first-name-filter"
            value={filters.first_name}
            onChange={(event) => updateFilter("first_name", event.target.value)}
            placeholder="Celeste"
          />
        </label>

        <label htmlFor="last-name-filter">
          <span>Last name</span>
          <input
            id="last-name-filter"
            value={filters.last_name}
            onChange={(event) => updateFilter("last_name", event.target.value)}
            placeholder="Fowkes"
          />
        </label>

        <label htmlFor="state-filter">
          <span>State</span>
          <select
            id="state-filter"
            value={filters.state}
            onChange={(event) => updateFilter("state", event.target.value)}
          >
            <option value="">Any state</option>
            {filterOptions.states.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
        </label>

        <label htmlFor="diagnosis-filter">
          <span>Diagnosis</span>
          <select
            id="diagnosis-filter"
            value={filters.diagnosis}
            onChange={(event) => updateFilter("diagnosis", event.target.value)}
          >
            <option value="">Any diagnosis</option>
            {filterOptions.diagnoses.map((diagnosis) => (
              <option key={diagnosis} value={diagnosis}>
                {diagnosis}
              </option>
            ))}
          </select>
        </label>

        <label htmlFor="gene-filter">
          <span>Gene</span>
          <select
            id="gene-filter"
            value={filters.gene}
            onChange={(event) => updateFilter("gene", event.target.value)}
          >
            <option value="">Any gene</option>
            {filterOptions.genes.map((gene) => (
              <option key={gene} value={gene}>
                {gene}
              </option>
            ))}
          </select>
        </label>

        <button className="icon-button" type="button" onClick={resetFilters} title="Reset filters">
          <RotateCcw size={18} aria-hidden="true" />
        </button>
      </section>

      {error ? <div className="error-banner">{error}</div> : null}

      <section className="workspace">
        <div className="results-panel">
          <div className="panel-heading">
            <div>
              <h2>Patients</h2>
              <p>{isLoadingPatients ? "Loading records" : `${patients.length} records shown`}</p>
            </div>
            <Search size={20} aria-hidden="true" />
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>State</th>
                  <th>Diagnosis</th>
                  <th>Genes</th>
                </tr>
              </thead>
              <tbody>
                {isLoadingPatients ? (
                  <tr>
                    <td colSpan={4} className="empty-cell">
                      <Loader2 className="spin" size={18} aria-hidden="true" />
                      Loading patients
                    </td>
                  </tr>
                ) : patients.length ? (
                  patients.map((patient) => (
                    <tr
                      key={patient.patient_id}
                      className={patient.patient_id === selectedPatientId ? "selected-row" : ""}
                      onClick={() => setSelectedPatientId(patient.patient_id)}
                    >
                      <td>
                        <button type="button" className="patient-link">
                          {patient.last_name}, {patient.first_name}
                        </button>
                        <small>{patient.patient_id}</small>
                      </td>
                      <td>{patient.state}</td>
                      <td>{patient.diagnosis}</td>
                      <td>
                        <GeneList genes={patient.genes} />
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={4} className="empty-cell">
                      No patients match the current filters
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        <aside className="detail-panel" aria-label="Selected patient details">
          <div className="panel-heading">
            <div>
              <h2>Patient Detail</h2>
              <p>{selectedPatient ? selectedPatient.patient_id : "No patient selected"}</p>
            </div>
            <ClipboardList size={20} aria-hidden="true" />
          </div>

          {isLoadingPatient ? (
            <div className="detail-empty">
              <Loader2 className="spin" size={20} aria-hidden="true" />
              Loading patient
            </div>
          ) : selectedPatient ? (
            <PatientDetailView patient={selectedPatient} />
          ) : (
            <div className="detail-empty">Select a patient from the table</div>
          )}
        </aside>
      </section>
    </main>
  );
}

function GeneList({ genes }: { genes: string[] }) {
  if (!genes.length) {
    return <span className="muted">None</span>;
  }

  return (
    <div className="gene-list">
      {genes.map((gene) => (
        <span key={gene}>{gene}</span>
      ))}
    </div>
  );
}

function PatientDetailView({ patient }: { patient: PatientDetail }) {
  return (
    <div className="patient-detail">
      <div className="identity">
        <div className="avatar">
          <UserRound size={26} aria-hidden="true" />
        </div>
        <div>
          <h3>
            {patient.first_name} {patient.last_name}
          </h3>
          <p>{patient.gender}</p>
        </div>
      </div>

      <dl className="detail-grid">
        <div>
          <dt>Phone</dt>
          <dd>{patient.phone}</dd>
        </div>
        <div>
          <dt>Location</dt>
          <dd>
            {patient.city}, {patient.state} {patient.zip_code}
          </dd>
        </div>
        <div className="full-row">
          <dt>Address</dt>
          <dd>
            <MapPin size={16} aria-hidden="true" />
            {patient.street_address}
          </dd>
        </div>
        <div>
          <dt>Diagnosis</dt>
          <dd>{patient.diagnoses.join(", ")}</dd>
        </div>
        <div>
          <dt>Genes</dt>
          <dd>
            <GeneList genes={patient.genes} />
          </dd>
        </div>
      </dl>
    </div>
  );
}
