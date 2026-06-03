VENV_PYTHON = $(CURDIR)/.venv/bin/python
VIEWER_PORT = 5173
PROXY_PORT  = 8765

.PHONY: start stop install

start:
	python start.py

stop:
	@pkill -f "server/gemini_proxy.py" 2>/dev/null || true
	@lsof -ti:$(VIEWER_PORT) | xargs kill -9 2>/dev/null || true
	@echo "Stopped."

install:
	python3 -m venv .venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install websockets google-genai pydantic python-dotenv opencv-python-headless numpy requests
	cd viewer && npm install
	@echo "Done. Set GEMINI_API_KEY in .env then run 'make start'."
