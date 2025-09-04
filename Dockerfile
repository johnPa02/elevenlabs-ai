ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    ffmpeg \
    libportaudio2 portaudio19-dev libasound2-dev libsndfile1 \
 && rm -rf /var/lib/apt/lists/*

# Install uv for fast, deterministic installs from pyproject/uv.lock
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Only copy project metadata first to maximize layer cache
COPY pyproject.toml uv.lock ./

# Install dependencies in a project-local venv (.venv)
RUN uv sync --frozen --no-dev --python python

# Now copy the full source
COPY . .

EXPOSE 8000

# Start FastAPI server
CMD ["uv", "run", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

