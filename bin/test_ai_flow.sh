#!/data/data/com.termux/files/usr/bin/bash
clear
echo "========================================="
echo "   BATERIA DE TESTES: IA TERMIRIS       "
echo "========================================="
echo ""

# Teste 1: Infraestrutura Básica
echo "[TESTE 1/3] Verificando processos de fundo..."
if tmux has-session -t ia_chat 2>/dev/null; then
    echo "  🟢 Sessão tmux 'ia_chat' está rodando."
else
    echo "  🔴 Erro: Sessão 'ia_chat' não encontrada. Tentando iniciar..."
    ~/.termiris/bin/ai >/dev/null 2>&1
    sleep 1
fi

if pgrep -f "entr.*update_context" >/dev/null; then
    echo "  🟢 Monitor 'entr' está escutando alterações."
else
    echo "  🔴 Erro: Monitor 'entr' está desligado."
fi
echo ""

# Teste 2: Injeção de Contexto (Simulação)
echo "[TESTE 2/3] Simulando salvamento de arquivo de código..."
TEST_FILE="/data/data/com.termux/files/home/.termiris_test_ia.py"
echo "# Código de teste do Termiris" > "$TEST_FILE"
echo "def termiris_funcao_secreta():" >> "$TEST_FILE"
echo "    return 'Automação Máxima Ativada'" >> "$TEST_FILE"

echo "  -> Modificando arquivo temporário para disparar o monitor..."
~/.termiris/bin/update_context.sh "$TEST_FILE"
rm -f "$TEST_FILE"
echo "  🟢 Injeção executada com sucesso."
echo ""

# Teste 3: Interação Humana
echo "[TESTE 3/3] Validação de Contexto Ativo no Chat"
echo "--------------------------------------------------------"
echo "Instruções para você, Íris:"
echo "1. Eu vou te jogar para dentro do Chat da IA agora."
echo "2. Pergunte exatamente isto para ela:"
echo "   'Qual o nome da função secreta do arquivo python de teste?'"
echo "3. Se ela responder 'termiris_funcao_secreta', o fluxo está 100%!"
echo "4. Pressione ESC para sair do chat e finalizar."
echo "--------------------------------------------------------"
read -p "Pressione [ENTER] para entrar no chat e testar..."

tmux switch-client -t ia_chat 2>/dev/null || tmux attach-session -t ia_chat
