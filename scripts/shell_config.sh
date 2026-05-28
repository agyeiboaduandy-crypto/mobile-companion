# Mobile Companion Shell Aliases

# Load environment variables
if [ -f "$HOME/.mobile-companion.env" ]; then
    export $(grep -v '^#' "$HOME/.mobile-companion.env" | xargs)
fi

# Aliases for AI Tools
alias ai-open='opencode'
alias ai-ollama='curl -X POST http://localhost:11434/api/generate -d'
alias ai-models='cat ~/.mobile-companion-models'
alias ai-update-models='bash ~/mobile-companion/scripts/fetch_models.sh'



# Quick setup command
alias ai-setup='bash ~/mobile-companion/scripts/setup_termux.sh'
alias ai-keys='bash ~/mobile-companion/scripts/manage_keys.sh'

echo "Mobile Companion AI aliases loaded."
