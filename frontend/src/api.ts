export type PatientSummary = {
  patient_id: string;
  first_name: string;
  last_name: string;
  gender: string;
  city: string;
  state: string;
  diagnosis: string;
  genes: string[];
};

export type PatientDetail = {
  patient_id: string;
  first_name: string;
  last_name: string;
  gender: string;
  street_address: string;
  city: string;
  state: string;
  zip_code: string;
  phone: string;
  diagnoses: string[];
  genes: string[];
};

export type FilterOptions = {
  states: string[];
  diagnoses: string[];
  genes: string[];
};

export type PatientFilters = {
  first_name: string;
  last_name: string;
  state: string;
  diagnosis: string;
  gene: string;
};

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchFilterOptions(): Promise<FilterOptions> {
  return getJson<FilterOptions>("/api/filters");
}

export function fetchPatients(filters: PatientFilters): Promise<PatientSummary[]> {
  const params = new URLSearchParams();

  Object.entries(filters).forEach(([key, value]) => {
    const trimmed = value.trim();
    if (trimmed) {
      params.set(key, trimmed);
    }
  });

  const query = params.toString();
  return getJson<PatientSummary[]>(`/api/patients${query ? `?${query}` : ""}`);
}

export function fetchPatient(patientId: string): Promise<PatientDetail> {
  return getJson<PatientDetail>(`/api/patients/${patientId}`);
}
