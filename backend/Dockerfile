# Dockerfile per il backend FastAPI
FROM python:3.12-slim

# Imposta variabili d'ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crea utente non-root per sicurezza
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Imposta directory di lavoro
WORKDIR /app

# Copia requirements e installa dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY . .

# Cambia proprietario dei file
RUN chown -R appuser:appuser /app

# Cambia a utente non-root
USER appuser

# Espone la porta
EXPOSE 8000

# Comando di avvio
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
