# Frontend

React and TypeScript dashboard for uploading boxing videos, creating analysis
jobs, polling job state, and presenting results when the vision worker is added.

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to `http://localhost:8000` in development. Set
`VITE_API_BASE_URL` when the API is hosted elsewhere.

```bash
npm run lint
npm test
npm run build
```
