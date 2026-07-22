#!/data/data/com.termux/files/usr/bin/bash

ARQUIVO="$1"
MAX_SIZE=200000

LOG="$HOME/.termiris/tmp/update_context.log"
AILOG="$HOME/.termiris/tmp/aichat.log"
LOCK="$HOME/.termiris/tmp/ctx.lock"

mkdir -p "$HOME/.termiris/tmp"

exec 9>"$LOCK"
flock -n 9 || exit 0

{
    echo
    echo "============================================================"
    echo "$(date)"
    echo "update_context.sh chamado com: $ARQUIVO"
} >> "$LOG"

if [ -f "$ARQUIVO" ]; then
    TAMANHO=$(wc -c < "$ARQUIVO")
    echo "Tamanho: $TAMANHO bytes" >> "$LOG"

    if [ "$TAMANHO" -lt "$MAX_SIZE" ]; then

        {
            echo
            echo "============================================================"
            echo "$(date)"
            echo "Arquivo: $(realpath "$ARQUIVO")"
            echo
            cat "$ARQUIVO"
        } | aichat -s termiris_ctx >> "$AILOG" 2>&1

        STATUS=$?

        if [ "$STATUS" -eq 0 ]; then
            echo "API: 🟢 OK" >> "$LOG"
        else
            echo "API: 🔴 ERRO ($STATUS)" >> "$LOG"
        fi
    else
        echo "Arquivo muito grande: $TAMANHO bytes" >> "$LOG"
    fi
else
    echo "Arquivo não encontrado: $ARQUIVO" >> "$LOG"
fi

echo "------------------------------------------------------------" >> "$LOG"
