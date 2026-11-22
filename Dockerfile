FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM --platform=linux/amd64 python:3.11-slim
WORKDIR /app
RUN useradd -m myuser
RUN rm -rf /usr/local/lib/python3.11/site-packages/setuptools/_vendor/* \
    && rm -rf /usr/local/lib/python3.11/site-packages/*.dist-info
COPY --chown=myuser:myuser --from=builder /usr/local /usr/local
COPY --chown=myuser:myuser . .
USER myuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "8080", "--workers", "1"]