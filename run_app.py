import subprocess
import os
import sys
import time

def run_application():
    # Define paths based on your folder structure
    root_path = os.getcwd()
    backend_path = os.path.join(root_path, "backend")
    frontend_path = os.path.join(root_path, "frontend")

    print("--- Initializing Full-Stack AI System ---")

    # 1. Start the Backend API
    print("Starting Backend API (FastAPI)...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "api.py"],
            cwd=backend_path,
            shell=True
        )
    except Exception as e:
        print(f"Failed to start backend: {e}")
        return

    # Brief pause to let the API initialize
    time.sleep(2)

    # 2. Start the Frontend Development Server
    print("Starting Frontend (Vite/React)...")
    try:
        # 'shell=True' is required for npm commands on Windows
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_path,
            shell=True
        )
    except Exception as e:
        print(f"Failed to start frontend: {e}")
        backend_process.terminate()
        return

    print("\n--- System Operational ---")
    print("Backend: http://127.0.0.1:8000")
    print("Frontend: Check terminal for Vite URL (usually http://localhost:5173)")
    print("Press CTRL+C in this window to stop both servers.")

    try:
        # Keep the main script running while the processes are active
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Done.")

if __name__ == "__main__":
    run_application()