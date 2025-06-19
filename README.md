# Rate limits

https://ai.google.dev/gemini-api/docs/rate-limits#free-tier

for Gemini 2.0 Flash
- RPM: 15
- TPM: 1,000,000
- RPD: 1,500

# How to use

api_key: <str>
messages: [
    {"role": "system", "content": "Bạn là một trợ lý hữu ích."},
    {"role": "user", "content": "Hãy giới thiệu bản thân"}
]
model: gemini-2.0-flash as default

# Run

uvicorn server:app --host 0.0.0.0 --port <PORT> [--reload]
POST http://<YOUR_IP>:<PORT>/chat
docs: http://<YOUR_IP>:<PORT>/docs
