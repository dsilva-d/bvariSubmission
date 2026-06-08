# React Frontend

## Setup

```bash
npm install
```

Run this once before starting the frontend. It recreates `node_modules`, which is
not included in the submission package.

## Run

Start the Flask API first from the project root:

```bash
source .venv/bin/activate
flask --app backend.app run --debug
```

Then start the React frontend from this directory:

```bash
npm run dev
```

Open `http://127.0.0.1:5173`.

The Vite dev server proxies `/api` requests to `http://127.0.0.1:5000`.

If `npm run dev` reports `vite: command not found`, run `npm install` in this
directory and try again.

## Build

```bash
npm run build
```
