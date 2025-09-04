## ElevenLabs AI - Server Tools

This project provides utilities and a simple FastAPI server to expose server tools for ElevenLabs Conversational AI integrations.

### Setup

1. Create a `.env` file with at least:

```
ELEVENLABS_API_KEY=...
AGENT_ID=...
VOICE_ID=...

# Expected values for confirm-identity server tool
EXPECTED_NAME=Nguyen Thi Cam
EXPECTED_CCCD=528981176214
EXPECTED_PHONE=0955423314
EXPECTED_DOB=18-09-1989

# Optional server tool behavior
MAX_RETRIES=2
SESSION_TTL_SECONDS=600
```

2. Install deps and run the API server:

```
uvicorn src.api.app:app --reload
```

### Endpoints

- `GET /health` → `{ "status": "ok" }`
- `POST /tools/confirm-identity`
  - Request JSON:
    - `name`, `cccd`, `phone`, `dob`, optional `session_id`
  - Response JSON:
    - `{ "verified": boolean, "locked": boolean }`

Example:

```
curl -X POST http://localhost:8000/tools/confirm-identity \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Nguyễn Thị Cam",
    "cccd": "528981176214",
    "phone": "0955423314",
    "dob": "18-09-1989",
    "session_id": "abc123"
  }'
```

### Code layout

- `src/api/` → FastAPI app and HTTP endpoints (server tools)
- `src/client/` → ElevenLabs client modules (agents, tools, phone numbers, pronunciation)
- `src/utils/` → Utilities such as prompt loading
- `src/prompts/` → Prompt templates
