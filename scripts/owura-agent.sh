#!/data/data/com.termux/files/usr/bin/bash

# OWURA - The AI Coding Agent (Vision 2.0)
# A lightweight, permanent mobile coding solution.

ENV_FILE="$HOME/.owura.env"
MODELS_FILE="$HOME/.owura-models"

# Load Environment
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# ASCII Art Banner
banner() {
    echo -e "\e[32m"
    echo "  ___   _   _  _   _  ___   ___ "
    echo " / _ \ | | | || | | | / _ \ / _ \"
    echo "| | | || | | || | | || | | | (_) |"
    echo "| |_| || |_| || |_| || |_| | \__, |"
    echo " \___/  \__, | \___/  \___/    /_/"
    echo "         __/ |                    "
    echo "        |___/                     "
    echo -e "\e[0m"
}

# Mode System
current_mode="CODER"
get_best_model() {
    if grep -q "GOOGLE_AI_STUDIO_KEY" "$ENV_FILE"; then
        echo "gemini-1.5-pro"
    elif grep -q "GROQ_API_KEY" "$ENV_FILE"; then
        echo "llama3-70b-8192"
    else
        echo "default"
    fi
}

# Termux:API Notification
notify() {
    termux-notification --title "OWURA" --content "$1"
}

# Main Agent Loop
clear
banner
echo -e "\e[32m>> System: Online\e[0m"
echo -e "\e[32m>> Mode: \e[1m$current_mode\e[0m"
echo -e "\e[32m>> Model: \e[1m$(get_best_model)\e[0m"
echo "--------------------------------------------------"
echo "Tuning options: [M]ode | [K]eys | [S]etup | [X]it"
echo "--------------------------------------------------"

while true; do
    read -p "OWURA@termux:~$ " cmd
    case $cmd in
        "exit"|"X"|"x") 
            notify "Session terminated. Goodbye."
            exit 0 ;;
        "M"|"m")
            echo "Select Mode: 1) ARCHITECT 2) CODER 3) SENTRY"
            read -p ">> " m_choice
            case $m_choice in
                1) current_mode="ARCHITECT"; echo "Mode set to ARCHITECT" ;;
                2) current_mode="CODER"; echo "Mode set to CODER" ;;
                3) current_mode="SENTRY"; echo "Mode set to SENTRY" ;;
            esac
            ;;
        "K"|"k")
            bash ~/owura/scripts/keys.sh ;;
        "S"|"s")
            bash ~/owura/scripts/setup.sh ;;
        *)
            # Pass everything else to opencode
            opencode --model $(get_best_model) --mode $current_mode "$cmd"
            ;;
    esac
done
