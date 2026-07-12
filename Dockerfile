FROM python:3.13-alpine@sha256:399babc8b49529dabfd9c922f2b5eea81d611e4512e3ed250d75bd2e7683f4b0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PATH=/opt/venv/bin:$PATH

RUN addgroup -S -g 10001 viasign \
    && adduser -S -D -H -u 10001 -G viasign viasign \
    && python -m venv /opt/venv

WORKDIR /app

COPY requirements.lock ./requirements.lock
RUN python -m pip install --no-cache-dir --requirement requirements.lock

COPY src ./src

USER 10001:10001
EXPOSE 10000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:10000/healthz', timeout=2).read()"

CMD ["python", "-m", "uvicorn", "viasign_parser.api:app", "--host", "0.0.0.0", "--port", "10000", "--no-access-log", "--no-server-header"]
