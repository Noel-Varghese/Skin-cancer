import subprocess
import sys
import time
from pathlib import Path


def run_application():
    # Base paths based on this script's location
    root_path = Path(__file__).resolve().parent
    backend_path = root_path / "backend"
    frontend_path = root_path / "frontend"

    is_windows = sys.platform.startswith("win")

    print("--- Initializing Full-Stack AI System ---")

    # ============================================================
    # START BACKEND
    # ============================================================

    print("Starting Backend API (FastAPI)...")

    try:
        backend_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "api:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
                "--reload"
            ],
            cwd=backend_path
        )

    except Exception as e:
        print(f"Failed to start backend: {e}")
        return

    # Give FastAPI time to initialize
    time.sleep(2)

    # ============================================================
    # START FRONTEND
    # ============================================================

    print("Starting Frontend (Vite/React)...")

    try:
        frontend_command = [
            "npm",
            "run",
            "dev"
        ]

        frontend_process = subprocess.Popen(
            frontend_command,
            cwd=frontend_path,
            shell=is_windows
        )

    except Exception as e:
        print(f"Failed to start frontend: {e}")

        backend_process.terminate()

        return

    # ============================================================
    # SYSTEM READY
    # ============================================================

    print("\n--- System Operational ---")
    print("Backend:  http://127.0.0.1:8000")
    print("API Docs: http://127.0.0.1:8000/docs")
    print("Frontend: Check terminal for Vite URL")
    print("\nPress CTRL+C to stop both servers.")

    # ============================================================
    # KEEP SERVERS RUNNING
    # ============================================================

    try:

        while True:

            if backend_process.poll() is not None:

                print("\nBackend stopped.")

                frontend_process.terminate()

                break

            if frontend_process.poll() is not None:

                print("\nFrontend stopped.")

                backend_process.terminate()

                break

            time.sleep(1)

    except KeyboardInterrupt:

        print("\nShutting down servers...")

        backend_process.terminate()
        frontend_process.terminate()

        backend_process.wait()
        frontend_process.wait()

        print("Done.")


if __name__ == "__main__":
    run_application()
