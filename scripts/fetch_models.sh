#!/data/data/com.termux/files/usr/bin/bash

# Model Fetcher for Mobile Companion
# This script queries providers for available models based on set API keys.

ENV_FILE="$HOME/.mobile-companion.env"
MODELS_FILE="$HOME/.mobile-companion-models"

fetch_google() {
    local key=$(grep "GOOGLE_AI_STUDIO_KEY=" "$ENV_FILE" | cut -d'=' -f2)
    if [ -n "$key" ]; then
        echo "Fetching Google AI Studio models..."
        curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$key" | jq -r '.models[].name' | sed 's/^models\//' > "$MODELS_FILE.google"
    fi
}

fetch_groq() {
    local key=$(grep "GROQ_API_KEY=" "$ENV_FILE" | cut -d'=' -f2)
    if [ -n "$key" ]; then
        echo "Fetching Groq models..."
        curl -s -H "Authorization: Bearer $key" "https://api.groq.com/openai/v1/models" | jq -r '.data[].id' > "$MODELS_FILE.groq"
    fi
}

fetch_nvidia() {
    local key=$(grep "NVIDIA_API_KEY=" "$ENV_FILE" | cut -d'=' -f2)
    if [ -n "$key" ]; then
        echo "Fetching NVIDIA models..."
        curl -s -H "Authorization: Bearer $key" "https://api.nvidia.com/v1/models" | jq -r '.data[].id' > "$MODELS_FILE.nvidia"
    fi
}

fetch_ollama() {
    local host=$(grep "OLLAMA_HOST=" "$ENV_FILE" | cut -d'=' -f2)
    if [ -n "$host" ]; then
        echo "Fetching Ollama models..."
        curl -s "$host/api/tags" | jq -r '.models[].name' > "$MODELS_FILE.ollama"
    fi
}

# Fetch all available
fetch_google
fetch_groq
fetch_nvidia
fetch_ollama

# Combine into a single readable file
echo "--- Available Models ---" > "$MODELS_FILE"
echo "[Google AI Studio]" >> "$MODELS_FILE"
cat "$MODELS_FILE.google" 2>/dev/null >> "$MODELS_FILE"
echo "" >> "$MODELS_FILE"
echo "[Groq]" >> "$MODELS_FILE"
cat "$MODELS_FILE.groq" 2>/dev/null >> "$MODELS_FILE"
echo "" >> "$MODELS_FILE"
echo "[NVIDIA]" >> "$MODELS_FILE"
cat "$MODELS_FILE.nvidia" 2>/dev/null >> "$MODELS_FILE"
echo "" >> "$MODELS_FILE"
echo "[Ollama]" >> "$MODELS_FILE"
cat "$MODELS_FILE.ollama" 2>/dev/null >> "$MODELS_FILE"

# Cleanup temp files
rm -f "$MODELS_FILE".*

echo "Models updated in $MODELS_FILE"
cat "$MODELS_FILE"
