FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PORT=8080

WORKDIR /app

COPY pyproject.toml .

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


COPY app ./app

EXPOSE 8080

CMD ["uv", "run", "python", "-m", "app/main.py"]