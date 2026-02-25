import os
import subprocess
import sys
import time
import requests

def run_backend():
    print("Starting Backend (FastAPI)...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return backend_process

def run_frontend():
    print("Starting Frontend (Streamlit)...")
    frontend_process = subprocess.Popen(
        ["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return frontend_process

if __name__ == "__main__":
    b_proc = run_backend()
    
    # Wait for backend to be ready
    print("Waiting for backend to initialize...")
    max_retries = 10
    while max_retries > 0:
        try:
            response = requests.get("http://localhost:8000/")
            if response.status_code < 500:
                print("Backend is live.")
                break
        except:
            pass
        time.sleep(2)
        max_retries -= 1
        
    f_proc = run_frontend()
    
    try:
        while True:
            # Monitor processes
            if b_proc.poll() is not None:
                print("Backend process died.")
                break
            if f_proc.poll() is not None:
                print("Frontend process died.")
                break
            time.sleep(5)
    except KeyboardInterrupt:
        print("Shutting down...")
        b_proc.terminate()
        f_proc.terminate()
