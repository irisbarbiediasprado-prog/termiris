Contrato do parser.sock para Eventos Estruturados

Arquitetura:

- parser.sock = transporte de eventos (MITL -> Python)
- EventBus = distribuicao interna (Python -> multiplos consumidores)
- MITL (C) emite JSON Lines para o socket
- EventBus (Python) le do socket e publica internamente

Formato da Mensagem:

Mensagens sao JSON, uma por linha, com versao.

Exemplo:

{
  "version": 1,
  "type": "COMMAND_STARTED",
  "session": "ia_chat",
  "pane": "Chat",
  "payload": {
    "command": ".file /path/snapshot.ctx"
  }
}

Tipos de Evento:

COMMAND_STARTED  -> comando iniciado          -> payload: {"command": string}
OUTPUT_RECEIVED  -> saida gerada              -> payload: {"output": string}
WAITING_INPUT    -> aguardando entrada        -> payload: {"prompt": string}
INPUT_RECEIVED   -> entrada enviada           -> payload: {"input": string}
COMMAND_FINISHED -> comando terminou          -> payload: {"exit_code": int}
ERROR            -> erro detectado            -> payload: {"error": string}
AGENT_STARTED    -> agente iniciou            -> payload: {"agent": string}
AGENT_WAITING    -> agente aguarda aprovacao  -> payload: {"reason": string}
AGENT_COMPLETED  -> agente concluiu           -> payload: {"result": string}
AGENT_FAILED     -> agente falhou             -> payload: {"error": string}

Fluxo Completo (comando .file):

1) { "version":1, "type":"COMMAND_STARTED", "session":"ia_chat", "pane":"Chat", "payload":{"command":".file snapshot.ctx"} }
2) { "version":1, "type":"OUTPUT_RECEIVED", "payload":{"output":"termiris_ctx)"} }
3) { "version":1, "type":"WAITING_INPUT", "payload":{"prompt":"termiris_ctx)"} }
4) { "version":1, "type":"INPUT_RECEIVED", "payload":{"input":"echo ok"} }
5) { "version":1, "type":"COMMAND_FINISHED", "payload":{"exit_code":0} }

Agente solicitando aprovacao:

{ "version":1, "type":"AGENT_WAITING", "payload":{"reason":"Delete file? (y/n)"} }

Evolucao Futura:
- Adicionar campo "metadata" no topo (ex: pid, cwd)
- Suporte a multiplos produtores (outros agentes)
- Replay de eventos para recovery
