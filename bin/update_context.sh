#!/data/data/com.termux/files/usr/bin/bash
# update_context.sh corrigido - Passagem limpa via redirecionamento de arquivo
ARQUIVO="$1"
MAX_SIZE=200000

if [ ! -f "$ARQUIVO" ]; then
    exit 0
fi

LOCKFILE="/data/data/com.termux/files/usr/tmp/ctx.lock"
exec 9>"$LOCKFILE"
if ! flock -n 9; then
    exit 0
fi

TAMANHO=$(wc -c < "$ARQUIVO")
if [ "$TAMANHO" -lt "$MAX_SIZE" ]; then
    # Usando o parâmetro -f do aichat para injetar o arquivo sem emular digitação no chat ativo
    aichat -s termiris_ctx -f "$ARQUIVO" --dry-run > /dev/null 2>&1
    
    # Alimentação complementar via append silencioso na sessão
    {
        echo "--- CONTEXTO ATUALIZADO ($(date '+%H:%M:%S')) ---"
        echo "Arquivo: $(realpath "$ARQUIVO")"
        echo "Conteúdo:"
        cat "$ARQUIVO"
    } | aichat -s termiris_ctx > /dev/null 2>&1
fi
