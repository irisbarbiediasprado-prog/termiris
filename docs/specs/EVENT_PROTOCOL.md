EVENT_PROTOCOL.md

«Status: Draft
Version: 1.0
Audience: MITL, Protocol Runtime, Runtime Engine, Eval Framework»

---

Objetivo

O Event Protocol define como os componentes do Termiris comunicam fatos observáveis.

Este documento não define implementação.

Não define sockets.

Não define JSONL.

Não define Python.

Não define C.

Ele define apenas o contrato entre produtores e consumidores de eventos.

---

Filosofia

Eventos representam fatos.

Nunca intenções.

Nunca planos.

Nunca comandos.

Nunca efeitos futuros.

Quando um evento existe, significa que aquele fato ocorreu.

---

Princípios

1. Imutabilidade

Um evento nunca é alterado.

Se o estado mudar, um novo evento deve ser produzido.

---

2. Responsabilidade

Cada componente publica apenas os fatos que ele próprio produz.

Exemplos:

- ProtocolExtractor publica "tag.detected"
- ProtocolRuntime publica "operation.generated"
- RuntimeEngine publica "operation.started"
- RuntimeEngine publica "operation.finished"
- Retriever publica "resource.resolved"

Nenhum componente publica eventos em nome de outro.

---

3. Transporte Independente

Eventos não conhecem:

- sockets
- arquivos
- JSONL
- stdout
- dashboards
- tp-judge

Esses mecanismos pertencem à infraestrutura.

---

4. Persistência Independente

Eventos podem ser:

- descartados
- gravados
- enviados pela rede
- agregados
- reduzidos

sem alterar o domínio.

---

5. Baixo Acoplamento

O produtor desconhece:

- quem irá consumir
- quantos consumidores existem
- onde os eventos serão armazenados

O produtor apenas registra o fato.

---

Envelope

Todo evento possui o mesmo envelope.

{
  "version": 1,
  "event_id": "...",
  "trace_id": "...",
  "timestamp": "...",
  "source": "...",
  "type": "...",
  "payload": {}
}

version

Versão do contrato.

Não representa versão do software.

---

event_id

Identificador único do evento.

Nunca reutilizado.

---

trace_id

Identifica uma cadeia causal.

Todos os eventos originados da mesma requisição compartilham o mesmo trace.

---

timestamp

Instante em que o fato ocorreu.

---

source

Componente que produziu o evento.

Exemplos:

- terminal
- protocol
- kernel
- runtime
- retriever

---

type

Nome do fato observado.

Exemplos:

- tag.detected
- operation.generated
- operation.started
- operation.finished
- resource.resolved

---

payload

Informações específicas daquele tipo de evento.

O payload deve conter apenas informações que não possam ser derivadas de outros eventos.

---

Catálogo Inicial

tag.detected

Source

protocol

Descrição

Uma tag válida foi identificada pelo ProtocolExtractor.

Payload:

{
  "tag_id": "...",
  "raw_text": "<<RETRIEVE FILE foo.py>>"
}

---

operation.generated

Source

kernel

Descrição

Uma Operation foi produzida pelo ProtocolRuntime.

Payload:

{
  "operation_id": "...",
  "instruction": "SNAPSHOT"
}

---

operation.started

Source

runtime

Payload:

{
  "operation_id": "..."
}

---

operation.finished

Source

runtime

Payload:

{
  "operation_id": "...",
  "status": "success"
}

---

resource.resolved

Source

retriever

Payload:

{
  "operation_id": "...",
  "uri": "filesystem:///..."
}

---

Causalidade

O protocolo descreve relações de causa e efeito.

tag.detected
      │
      ▼
operation.generated
      │
      ▼
operation.started
      │
      ▼
resource.resolved
      │
      ▼
operation.finished

Nem todos os fluxos percorrem todas as etapas.

Eventos opcionais permanecem opcionais.

---

Consumidores

Consumidores observam eventos.

Nunca influenciam sua produção.

Exemplos:

- ProtocolRuntime
- JsonlEventSink
- tp-evidence
- tp-judge
- Dashboard
- Telemetria

Adicionar um novo consumidor não deve exigir alterações no produtor.

---

Compatibilidade

Mudanças permitidas:

- adicionar novos eventos
- adicionar novos campos
- adicionar novos consumidores

Mudanças proibidas:

- remover campos existentes
- alterar semântica de eventos
- reutilizar nomes para significados diferentes

---

Arquitetura

            Producers

 Terminal
 ProtocolExtractor
 ProtocolRuntime
 RuntimeEngine
 Retriever
        │
        ▼
    Event Transport
        │
        ├──────────────► ProtocolRuntime
        ├──────────────► JsonlEventSink
        ├──────────────► tp-evidence
        ├──────────────► Dashboard
        └──────────────► Future Consumers

---

Regra Fundamental

«O produtor registra fatos.»

«O transporte move fatos.»

«Os consumidores atribuem significado aos fatos.»

Nenhuma dessas responsabilidades deve cruzar a fronteira da outra.
