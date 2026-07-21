#!/data/data/com.termux/files/usr/bin/bash
[ -f ~/.termiris/lib/core.sh ] && . ~/.termiris/lib/core.sh

# --- Auto-start da IA do Termiris ---
# Inicializa a sessão ia_chat e o monitor entr em segundo plano caso não existam
if ! tmux has-session -t ia_chat 2>/dev/null; then
    ~/.termiris/bin/ai >/dev/null 2>&1
fi
