#!/data/data/com.termux/files/usr/bin/bash

ok(){ printf "🟢 %s\n" "$1"; }
err(){ printf "🔴 %s\n" "$1"; }
info(){ printf "ℹ️  %s\n" "$1"; }

CFG="$HOME/.config/aichat/config.yaml"

echo "=== 🤖 Diagnóstico da IA ==="

echo
echo "Configuração"

if [ -f "$CFG" ]; then
    ok "config.yaml"
else
    err "config.yaml"
    exit 1
fi

MODEL="$(awk '/^model:/{m=$2} END{print m}' "$CFG")"

if [ -n "$MODEL" ]; then
    ok "Modelo: $MODEL"
else
    err "Nenhum modelo configurado"
    exit 1
fi

echo
echo "Sessão"

if tmux has-session -t ia_chat 2>/dev/null; then
    ok "Sessão ia_chat"
else
    err "Sessão ia_chat"
fi

if pgrep -af aichat >/dev/null; then
    ok "Processo aichat"
else
    err "Processo aichat"
fi

echo
echo "Modelo"

TMP="$(mktemp)"
START=$(date +%s%3N)

if printf "ping\n" | aichat --no-stream >"$TMP" 2>&1; then
    END=$(date +%s%3N)
    LAT=$((END-START))

    ok "Modelo respondeu"
    info "Latência: ${LAT} ms"

    echo
    echo "Última resposta"
    tail -n 8 "$TMP"

    echo
    echo "Resultado"
    ok "IA operacional"
else
    END=$(date +%s%3N)
    LAT=$((END-START))

    err "Modelo não respondeu"
    info "Latência: ${LAT} ms"

    echo
    echo "Erro"
    cat "$TMP"

    echo
    echo "Resultado"
    err "IA indisponível"
    rm -f "$TMP"
    exit 1
fi

rm -f "$TMP"
