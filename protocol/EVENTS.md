# Termiris Events

Status: Draft

O MITL nunca interpreta texto.

O MITL apenas transforma a saída da IA em eventos.

Todo o restante do sistema (TP, relatórios, certificação)
consome somente eventos.

---

# Evento

Todo evento possui:

- timestamp
- tipo
- payload

Formato:

EVENT <TYPE>

campos...

---

# Eventos básicos

TEXT

Texto livre produzido pela IA.

Não participa da certificação.

Exemplo:

EVENT TEXT

content:
A estratégia será localizar o arquivo primeiro.

---

RETRIEVE

Solicitação do protocolo.

Exemplo:

EVENT RETRIEVE

verb:
SEARCH

arg:
context-builder

---

FILE_SENT

Arquivo enviado ao Chat.

EVENT FILE_SENT

path:
~/.termiris/cache/context/context.md

---

FILE_RECEIVED

Arquivo solicitado pela IA.

EVENT FILE_RECEIVED

path:
bin/context-builder

---

ERROR

Erro detectado pelo MITL.

EVENT ERROR

reason:
unknown-verb

---

# Regras

TEXT nunca invalida um teste.

A certificação considera apenas eventos.

A ordem dos eventos é preservada.

Eventos possuem timestamp.

