#!/data/data/com.termux/files/usr/bin/bash

# OWURA - The AI Coding Agent
# This is the main entry point for the mobile coding experience.

ENV_FILE="$HOME/.owura.env"
MODELS_FILE="$HOME/.owura-models"

# Load Environment
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Helper: Get the best available model
get_best_model() {
    # Priority: Google Gemini Pro -> Groq Llama 3 -> NVIDIA -> Ollama
    if grep -q "GOOGLE_AI_STUDIO_KEY" "$ENV_FILE"; then
        echo "gemini-1.5-pro"
    elif grep -q "GROQ_API_KEY" "$ENV_FILE"; then
        echo "llama3-70b-8192"
    else
        echo "default"
    fi
}

# Main Agent Loop
echo "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—"
echo "â•‘            OWURA AI CODING AGENT                â•‘"
echo "â•‘         Code Anywhere. Anytime.                 â•‘"
echo "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•"
echo ""
echo "System: Ready. Model: $(get_best_model)"
echo "Context: MCP Filesystem & GitHub active."
echo "--------------------------------------------------"
echo "Type 'exit' to leave or start coding!"
echo ""

# Launch opencode with the detected best model
# We wrap opencode to ensure it has the right context
opencode --model $(get_best_model)
