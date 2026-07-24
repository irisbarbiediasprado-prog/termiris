# Termiris Protocol Conformance (TP)

Status: Draft

Objetivo

Verificar se um agente implementa corretamente o
Termiris Protocol (TP).

Cada teste possui:

- Identificador
- Entrada
- Resposta esperada
- Critério de aprovação

---

## TP-001 — Arquivo desconhecido

Entrada

Edite AGENTS.md.

Esperado

<<RETRIEVE FILE AGENTS.md>>

Aprovação

- utiliza RETRIEVE
- utiliza FILE
- não inventa conteúdo

---

## TP-002 — Caminho desconhecido

Entrada

Edite o builder responsável pelo contexto.

Esperado

<<RETRIEVE SEARCH context-builder>>

ou

<<RETRIEVE SEARCH builder>>

Aprovação

- não inventa caminhos
- utiliza SEARCH

---

## TP-003 — Consumir SEARCH

Entrada

BEGIN SEARCH

STATUS: OK

bin/context-builder

END SEARCH

Esperado

<<RETRIEVE FILE bin/context-builder>>

Aprovação

- utiliza FILE
- utiliza o caminho retornado

---

## TP-004 — Consumir FILE

Entrada

BEGIN RETRIEVE

STATUS: OK

FILE: bin/context-builder

...

END FILE

END RETRIEVE

Esperado

Continuar a tarefa.

Aprovação

- não solicita novamente o mesmo arquivo

---

## TP-005 — Tratamento de erro

Entrada

BEGIN RETRIEVE

STATUS: ERROR

ERROR: FILE_NOT_FOUND

END RETRIEVE

Esperado

Solicitar SEARCH ou TREE.

Aprovação

- não repete exatamente o mesmo RETRIEVE

---

Resultado

PASS

Todos os testes aprovados.

FAIL

Qualquer teste reprovado.


---

## TP-006 — Estratégia consistente

Entrada

Quero alterar o builder responsável pelo contexto.

Não conheço o caminho.

Esperado

Se o agente declarar que utilizará SEARCH primeiro,
a primeira chamada do protocolo DEVE ser:

<<RETRIEVE SEARCH context-builder>>

Reprovação

- declarar SEARCH e executar FILE;
- declarar SEARCH e executar TREE;
- contradizer a estratégia declarada.

