import uvicorn
import socket
import os
import sys

def is_port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def main():
    # Render / Railway / Fly.io inject PORT via environment variable
    env_port = os.environ.get("PORT")
    is_production = env_port is not None

    if is_production:
        # PRODUCTION: bind to all interfaces so the platform can reach us
        port = int(env_port)
        host = "0.0.0.0"
        reload = False
        print(f"[*] PRODUCTION mode — Binding to {host}:{port}")
    else:
        # LOCAL DEV: try ports 8000, 8001, 8080
        host = "127.0.0.1"
        reload = True
        port = 8000
        for p in [8000, 8001, 8080, 3001]:
            if not is_port_in_use(host, p):
                port = p
                break
            else:
                print(f"[!] Port {p} is busy, trying next...")

        print(f"[*] LOCAL DEV mode — Launching on http://{host}:{port}")
        print(f"[*] Frontend (served by FastAPI): http://{host}:{port}/app/")
        print(f"[*] API Docs: http://{host}:{port}/docs")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )

if __name__ == "__main__":
    main()
