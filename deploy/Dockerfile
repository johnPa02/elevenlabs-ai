ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*


# Install uv for fast, deterministic installs from pyproject/uv.lock
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Expect build context at project root. Copy only metadata first to leverage cache.
COPY pyproject.toml uv.lock ./

# Install dependencies into a local venv
RUN uv sync --frozen --no-dev --python python

# Copy the full project into the image
COPY src ./src

EXPOSE 8000

# Start FastAPI server
CMD ["uv", "run", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

