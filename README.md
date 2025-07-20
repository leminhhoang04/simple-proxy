# Introduction

This repository provides a proxy service that alternates between APIs to help achieve higher usage limits.

For development purposes, the default model used is `gemini-2.5-flash`.

To customize the model or related settings, update the relevant variables in both `router.py` and `server.py`.

# Getting started

1. Create `api-key.json` based on `api-key.json.example` 

2. Run server

```bash
uvicorn server:app --host 0.0.0.0 --port <PORT> [--reload]
```

3. View FastAPI documents at docs: http://<YOUR_IP>:<PORT>/docs

# Rate limits

https://ai.google.dev/gemini-api/docs/rate-limits#free-tier

for Gemini 2.5 Flash
- RPM: 10
- TPM: 250,000
- RPD: 250
