#!/data/data/com.termux/files/usr/bin/bash

API="https://api.groq.com/openai/v1/models"

echo "=== 🤖 Diagnóstico da IA Termiris ==="

printf "%-18s" "Monitor:"
pgrep -f "entr.*update_context" >/dev/null \
    && echo "🟢 ATIVO" \
    || echo "🔴 INATIVO"

printf "%-18s" "Sessão tmux:"
tmux has-session -t ia_chat 2>/dev/null \
    && echo "🟢 ATIVA" \
    || echo "🔴 INATIVA"

printf "%-18s" "Modelo:"
aichat --role termiris_ctx --dry-run "ping" >/dev/null 2>&1 \
    && echo "🟢 OK" \
    || echo "🔴 FALHA"

printf "%-18s" "API Groq:"

HTTP=$(curl -s \
    -o /dev/null \
    -w "%{http_code}" \
    --max-time 5 \
    -H "Authorization: Bearer $GROQ_API_KEY" \
    "$API")

case "$HTTP" in
    200)
        echo "🟢 OK"
        ;;
    401)
        echo "🔴 Chave inválida"
        ;;
    429)
        echo "🟡 Limite atingido"
        ;;
    *)
        echo "🔴 HTTP $HTTP"
        ;;
esac
