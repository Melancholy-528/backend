#!/usr/bin/env bash
# ==============================================================================
# SIH26092 - AI-Driven Scheme Matching Platform
# Backend Startup Script
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================================"
echo " Starting SIH26092 Backend Service"
echo " Ministry of Social Justice & Empowerment (MoSJE)"
echo "======================================================================"

# 1. Check or activate Python virtual environment
if [ -d ".venv" ]; then
    echo "[+] Activating virtual environment (.venv)..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "[+] Activating virtual environment (venv)..."
    source venv/bin/activate
else
    echo "[!] Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "[+] Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 2. Check Ollama local LLM status
OLLAMA_URL="${OLLAMA_BASE_URL:-http://localhost:11434}"
echo "[+] Checking local Ollama LLM at $OLLAMA_URL..."

if curl -s -m 2 "$OLLAMA_URL/api/tags" > /dev/null 2>&1; then
    MODEL_NAME="${OLLAMA_MODEL:-qwen2.5-coder:3b}"
    echo "[✓] Ollama service is active."
    if curl -s "$OLLAMA_URL/api/tags" | grep -q "$MODEL_NAME"; then
        echo "[✓] Model '$MODEL_NAME' is installed and ready."
    else
        echo "[!] Model '$MODEL_NAME' not detected in Ollama."
        echo "    To pull the recommended model, run: ollama pull $MODEL_NAME"
        echo "    (The chatbot will automatically use verified database fallback if model is missing.)"
    fi
else
    echo "[!] Ollama is not running at $OLLAMA_URL."
    echo "    To start Ollama, run: ollama serve"
    echo "    (The chatbot will automatically use its verified rule-based database fallback.)"
fi

# 3. Environment defaults
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-8000}"
export OLLAMA_NUM_GPU="${OLLAMA_NUM_GPU:-0}"      # 0 runs cleanly on CPU/RAM, preventing Vulkan VRAM out-of-memory
export OLLAMA_NUM_THREADS="${OLLAMA_NUM_THREADS:-8}" # Utilize multicore CPU threads
export OLLAMA_TIMEOUT="${OLLAMA_TIMEOUT:-65.0}"

echo "----------------------------------------------------------------------"
echo " Host:        http://$HOST:$PORT"
echo " API Docs:    http://$HOST:$PORT/docs"
echo " Interactive: http://$HOST:$PORT/redoc"
echo " Schemes DB:  schemes.json ($(python3 -c 'import json; print(len(json.load(open("schemes.json"))))') schemes indexed)"
echo "----------------------------------------------------------------------"

# 4. Launch FastAPI with Uvicorn
exec uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
