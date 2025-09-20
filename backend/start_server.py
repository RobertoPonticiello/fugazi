#!/usr/bin/env python3
"""
Script di avvio per il server Finge Backend
Evita problemi con Cursor e doppi avvii
"""

import uvicorn
from config import get_host, get_port

if __name__ == "__main__":
    print("🚀 Avvio server Finge Backend...")
    print(f"📍 Host: {get_host()}")
    print(f"🔌 Porta: {get_port()}")
    print(f"🌐 URL: http://localhost:{get_port()}")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host=get_host(),
        port=get_port(),
        reload=False,  # Disabilitato per evitare problemi con Cursor
        log_level="info"
    )
