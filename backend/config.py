#!/usr/bin/env python3
"""
Configuration file for Finge Backend
"""

import os


def _get_bool_env(var_name: str, default: bool) -> bool:
    value = os.getenv(var_name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")

# Financial Modeling Prep API Configuration
# In produzione NON usare fallback; imposta FMP_API_KEY nell'ambiente
FMP_API_KEY = "XXXXX"  # usato solo in sviluppo quando DEBUG=True

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Settings
# In produzione: DEBUG=False, RELOAD=False (configurabili via env)
DEBUG = _get_bool_env("DEBUG", False)
RELOAD = _get_bool_env("RELOAD", False)

# CORS Configuration
# Imposta CORS_ORIGINS via env (lista separata da virgole) in produzione
_DEFAULT_CORS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080"
]

def get_cors_origins():
    cors_env = os.getenv("CORS_ORIGINS")
    if cors_env:
        return [o.strip() for o in cors_env.split(",") if o.strip()]
    return _DEFAULT_CORS

def get_api_key():
    """Recupera la API key. In produzione richiede env, in dev consente fallback."""
    key = os.getenv("FMP_API_KEY")
    if key:
        return key
    # Consenti fallback solo se DEBUG attivo esplicitamente
    if DEBUG and FMP_API_KEY and FMP_API_KEY != "":
        return FMP_API_KEY
    return None

def get_host():
    """Get host from environment variable or config"""
    return os.getenv("HOST", HOST)

def get_port():
    """Get port from environment variable or config"""
    return int(os.getenv("PORT", PORT))
