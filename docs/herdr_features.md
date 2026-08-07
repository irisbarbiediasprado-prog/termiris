# Análise de Features do Herdr para o Termiris

## Matriz de Valor

| Feature do Herdr | Valor para Termiris | Copiar? | Implementação |
|------------------|---------------------|---------|---------------|
| Eventos estruturados de terminal | ⭐⭐⭐⭐⭐ | Sim | MITL → parser.sock → EventBus |
| Estado do pane (working, idle, blocked) | ⭐⭐⭐⭐⭐ | Sim | TerminalEvent + parser.sock |
| API/socket para integração | ⭐⭐⭐⭐⭐ | Sim | Evoluir parser.sock (transporte) |
| Persistência de sessão | ⭐⭐⭐⭐ | Parcial | tmux já resolve |
| Multiplexação | ⭐⭐ | Não | tmux já faz |
| IA embutida no terminal | ⭐⭐⭐ | Parcial | manter via aichat |
| Agentes controlando terminal | ⭐⭐⭐⭐ | Sim | Intent → Executor |
| Skills de agentes | ⭐⭐⭐⭐ | Sim | futuro no planner |
| UI moderna | ⭐ | Não agora | custo alto no mobile |
| Gestos/mouse | ⭐ | Não | Android + extra-keys é melhor |
| Configuração declarativa | ⭐⭐⭐⭐ | Sim | talvez termiris.toml |

## Camadas Arquiteturais

| Camada | Componente | Responsabilidade |
|--------|-----------|------------------|
| Transporte de sessão | tmux | Gerenciar janelas/panes no terminal |
| Percepção | MITL (C) | Observar PTY e emitir eventos |
| Transporte de eventos | parser.sock | Canal JSON Lines entre C e Python |
| Distribuição | EventBus (Python) | Rotear eventos para consumidores internos |
| Decisão | Runtime | Processar eventos, gerar Intents |
| Intenção | Planner | Definir plano de ação |
| Ação | Executor | Executar operações (ISA) |

## Prioridades de Implementação

- ✅ **Commit 1**: TerminalEvent + EventBus
- 🔜 **Commit 2** (documentação): HERDR_FEATURES.md + socket_contract.md
- 🔜 **Commit 3**: MITL emite JSON Lines no parser.sock
- 🔜 **Commit 4**: Python consome parser.sock e converte para TerminalEvent
- 🔜 **Commit 5**: Runtime reage a eventos via Intent

## Decisão Arquitetural

- Herdr é **documento de requisitos**, não dependência.
- Termiris evolui para "terminal agent-native" via eventos estruturados.
- tmux permanece backend (funciona no Termux).
- MITL se torna sensor inteligente do terminal.
- parser.sock é **transporte**, EventBus é **distribuição**.
