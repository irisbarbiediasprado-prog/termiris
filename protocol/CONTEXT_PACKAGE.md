# Context Package v1

## Objetivo

O Context Package (.ctx) é o formato oficial de troca de contexto do Termiris.

Todo handler que produz contexto gera exatamente um pacote.

Nenhum handler deve depender do formato textual produzido por outro handler.

---

## Estrutura

version: 1

session: TP-001

producer: retrieve-handler

timestamp: ISO-8601

metadata:
  verb:
  arg:

summary: |
  Resumo opcional.

files:

references:

payload: |
  Conteúdo integral.

---

## Garantias

- version é obrigatório.
- session é obrigatória.
- producer é obrigatório.
- payload é obrigatório.
- metadata é opcional.
- summary é opcional.
- files é opcional.
- references é opcional.

---

## Localização

cache/context/

000001.ctx
000002.ctx
...

---

## Fluxo

Handler
    ↓
Context Package
    ↓
State Handler
    ↓
Report
Notification
Replay
AI
