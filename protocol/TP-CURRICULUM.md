# Termiris Protocol Curriculum (TP)

Status: Draft

Objetivo

Ensinar um agente a trabalhar em projetos utilizando o
Termiris Protocol (TP).

O protocolo existe para eliminar suposições.

Sempre que faltar informação:

Pare.

Solicite contexto.

Nunca invente.

---

## Regra 1 — Arquivos

Se você não conhece o conteúdo de um arquivo:

NÃO invente.

Solicite-o.

Exemplo

Usuário

Edite AGENTS.md.

Resposta

<<RETRIEVE FILE AGENTS.md>>

---

## Regra 2 — Caminhos

Se você não conhece o caminho de um arquivo:

Não chute.

Descubra.

Exemplo

Usuário

Edite o builder responsável pelo contexto.

Resposta

<<RETRIEVE SEARCH context-builder>>

---

## Regra 3 — SEARCH → FILE

Quando SEARCH retornar um caminho válido,
solicite o arquivo.

Exemplo

BEGIN SEARCH

STATUS: OK

bin/context-builder

END SEARCH

Resposta

<<RETRIEVE FILE bin/context-builder>>

---

## Regra 4 — FILE → Trabalho

Quando FILE retornar com sucesso:

Leia.

Analise.

Continue a tarefa.

Não solicite novamente o mesmo arquivo.

---

## Regra 5 — Erros

Quando receber

STATUS: ERROR

não repita exatamente a mesma solicitação.

Exemplos

FILE
↓

SEARCH

SEARCH
↓

TREE

---

## Regra 6 — Contexto mínimo

Solicite apenas o necessário.

Prefira:

SEARCH

antes de

TREE

Prefira:

FILE

antes de

TREE .

---

## Regra 7 — Não invente

O agente nunca deve:

- inventar caminhos;
- inventar arquivos;
- inventar conteúdo;
- assumir arquitetura.

Quando houver dúvida:

Use o protocolo.

---

## Fluxo mental

Não sei o caminho

↓

<<RETRIEVE SEARCH ...>>

↓

Recebi o caminho

↓

<<RETRIEVE FILE ...>>

↓

Recebi o arquivo

↓

Analisar

↓

Implementar

---

Resumo

Quando faltar informação:

Não pense.

Não suponha.

Use TP.

---

## Lei Fundamental

O protocolo substitui suposições.

Quando uma informação necessária não estiver disponível:

1. Interrompa o raciocínio.
2. Solicite somente a informação necessária utilizando TP.
3. Aguarde a resposta.
4. Continue a tarefa.

Nunca preencha lacunas com conhecimento presumido.

Mantra

Quando faltar contexto:

Pare.

Recupere.

Continue.

