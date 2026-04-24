FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[dev]"

COPY src/ ./src/
COPY alembic.ini ./
COPY alembic/ ./alembic/

EXPOSE 8000
CMD ["uvicorn", "kindin_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
