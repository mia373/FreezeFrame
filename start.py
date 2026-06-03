#!/usr/bin/env python3
"""Cross-platform start script — launches the voice proxy and viewer together."""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent


def kill_port(port):
    if sys.platform == "win32":
        result = subprocess.run(
            f"netstat -ano | findstr :{port}",
            shell=True, capture_output=True, text=True,
        )
        pids = set()
        for line in result.stdout.splitlines():
            parts = line.split()
            if parts and parts[-1].isdigit():
                pids.add(parts[-1])
        for pid in pids:
            subprocess.run(f"taskkill /PID {pid} /F", shell=True, capture_output=True)
    else:
        subprocess.run(
            f"lsof -ti:{port} | xargs kill -9 2>/dev/null || true",
            shell=True, capture_output=True,
        )


def main():
    print("══ Clearing ports 8765 and 5173...")
    kill_port(8765)
    kill_port(5173)
    time.sleep(0.5)

    print("══ Starting Gemini Live proxy on ws://localhost:8765...")
    proxy = subprocess.Popen([sys.executable, "server/gemini_proxy.py"], cwd=ROOT)
    time.sleep(1)

    print("══ Starting viewer on http://localhost:5173...")
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    viewer = subprocess.Popen([npm, "run", "dev"], cwd=ROOT / "viewer")

    try:
        viewer.wait()
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        proxy.terminate()
        viewer.terminate()


if __name__ == "__main__":
    main()
