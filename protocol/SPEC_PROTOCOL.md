# Termiris Protocol (TP)

Status: Draft
Version: 0.1
Author: Termiris
Content-Type: text/plain

---

# 1. Objetivo

O Termiris Protocol (TP) define como um agente conversa com o ambiente
Termiris.

Todo comando deve ser:

- determinístico;
- idempotente quando possível;
- legível por humanos;
- legível por máquinas.

O protocolo é orientado a texto puro.

---

# 2. Estrutura

Um comando possui a forma:

<<VERB TARGET ARGUMENTS...>>

Exemplos:

<<RETRIEVE FILE AGENTS.md>>

<<RETRIEVE TREE lib>>

<<RETRIEVE SEARCH context-builder>>

---

# 3. Respostas

Toda resposta possui delimitadores explícitos.

Formato:

BEGIN <TYPE>

STATUS: OK | ERROR

...

END <TYPE>

---

# 4. STATUS

STATUS: OK

A operação foi executada.

STATUS: ERROR

A operação falhou.

Quando ERROR estiver presente,
o campo ERROR é obrigatório.

---

# 5. ERROR

Códigos definidos:

FILE_NOT_FOUND

DIRECTORY_NOT_FOUND

INVALID_ARGUMENT

EMPTY_RESULT

PERMISSION_DENIED

NOT_IMPLEMENTED

INTERNAL_ERROR

---

# 6. RETRIEVE

Família responsável pela obtenção de informações.

## FILE

Solicita um ou mais arquivos.

Solicitação

<<RETRIEVE FILE README.md AGENTS.md>>

Resposta

BEGIN RETRIEVE

STATUS: OK

FILE: README.md

...

END FILE

FILE: AGENTS.md

...

END FILE

END RETRIEVE

---

## TREE

Retorna a árvore de um diretório.

<<RETRIEVE TREE lib>>

---

## SEARCH

Pesquisa por texto.

<<RETRIEVE SEARCH context-builder>>

---

## DIFF

Retorna diferenças.

<<RETRIEVE DIFF README.md>>

---

## STATUS

Estado do projeto.

<<RETRIEVE STATUS>>

---

# 7. Compatibilidade

Novos comandos nunca alteram a sintaxe existente.

Novas funcionalidades devem ser adicionadas como novos VERBs ou novos
TARGETs.

---

# 8. Futuro

VERBs planejados

PATCH

RUN

TEST

COMMIT

PLAN

APPLY

