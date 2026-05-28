#!/data/data/com.termux/files/usr/bin/bash

# API Key Manager for Mobile Companion

ENV_FILE="$HOME/.mobile-companion.env"

set_key() {
    local key_name=$1
    local key_value=$2
    
    if [ -f "$ENV_FILE" ]; then
        sed -i "s/^$key_name=.*/$key_name=$key_value/" "$ENV_FILE"
    else
        echo "$key_name=$key_value" >> "$ENV_FILE"
    fi
    echo "Set $key_name successfully."
    
    # Automatically fetch models when a key is updated
    bash ~/mobile-companion/scripts/fetch_models.sh
}

show_keys() {
    if [ -f "$ENV_FILE" ]; then
        cat "$ENV_FILE"
    else
        echo "No keys set yet."
    fi
}

case "$1" in
    set)
        set_key "$2" "$3"
        ;;
    list)
        show_keys
        ;;
    *)
        echo "Usage: $0 {set key_name value | list}"
        echo "Example: $0 set ANTHROPIC_API_KEY sk-ant-..."
        ;;
esac
