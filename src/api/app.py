from fastapi import FastAPI

from src.api.tools import router as tools_router


app = FastAPI(title="ElevenLabs Server", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


# Mount server tools under /tools prefix
app.include_router(tools_router)
