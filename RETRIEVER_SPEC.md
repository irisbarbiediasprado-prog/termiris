# Retriever Specification

Status: Draft

Version: 0.1

---

# Missão

Permitir que agentes descubram contexto incrementalmente.

O Retriever não produz contexto.

O Retriever decide quais Builders devem ser utilizados para produzir o contexto necessário.

---

# Princípios

- Recuperação incremental.
- Responsabilidade única.
- Operações determinísticas.
- Baixo custo.
- Baixa latência.
- Artefatos reproduzíveis.

Agentes não recebem o projeto.

Agentes exploram o projeto.

---

# Arquitetura

Agente

↓

Retriever

↓

Builders

↓

Processors (opcional)

↓

Artefato

↓

Agente

---

# Operações

## Workspace

retrieve(workspace)

Retorna informações do workspace atual.

---

## Current File

retrieve(current-file)

Retorna o arquivo atual.

---

## Related Files

retrieve(related-files)

Retorna arquivos semanticamente relacionados.

---

## Symbol

retrieve(symbol, NAME)

Retorna contexto relacionado a um símbolo.

Exemplo:

retrieve(symbol, update_context)

---

## Tree

retrieve(tree)

Retorna apenas a estrutura relevante do projeto.

---

## Knowledge

retrieve(knowledge)

Retorna conhecimento persistente.

Exemplos:

- AGENTS.md
- CONTEXT_SPEC.md
- README.md

---

## Git

retrieve(git-diff)

retrieve(git-status)

retrieve(commits)

---

## Logs

retrieve(log)

retrieve(history)

retrieve(diagnostics)

---

# Builders

O Retriever nunca produz contexto diretamente.

Toda recuperação deve ser delegada a um Builder.

Exemplos:

Builder(current-file)

Builder(related-files)

Builder(project-knowledge)

Builder(source)

---

# Processors

Processors enriquecem Builders.

Exemplos futuros:

- langextract
- git
- tree
- ripgrep
- cache

---

# Não Objetivos

O Retriever nunca:

- conversa com a IA;
- interpreta respostas;
- modifica arquivos;
- aplica patches;
- toma decisões arquiteturais.

Seu papel é apenas localizar o contexto correto.

---

# Futuro

O Retriever poderá ser utilizado por qualquer agente através de um protocolo comum.

Exemplo conceitual:

retrieve(current-file)

retrieve(symbol, update_context)

retrieve(git-diff)

retrieve(knowledge)

A implementação do protocolo é independente do modelo de IA utilizado.

---

# Objetivo Final

Permitir que agentes naveguem autonomamente por projetos utilizando operações pequenas, previsíveis e reproduzíveis.

O contexto deixa de ser enviado.

O contexto passa a ser descoberto.

---

# Milestone 2

Objetivo

Validar a recuperação incremental de contexto.

Hipótese

Um agente consegue concluir uma tarefa solicitando apenas o contexto necessário.

Escopo

Implementar apenas:

retrieve(current-file)

Fluxo esperado

Usuário

↓

Tarefa

↓

Agente

↓

retrieve(current-file)

↓

Retriever

↓

Builder(current-file)

↓

Conteúdo do arquivo

↓

Agente

↓

Resposta

Critério de sucesso

- O usuário informa apenas a tarefa.
- Nenhum arquivo é enviado inicialmente.
- O agente solicita retrieve(current-file).
- O Retriever fornece o arquivo.
- O agente continua a tarefa normalmente.

Não objetivos

- related-files
- symbol
- knowledge
- Patch Engine
- LangExtract

Esses componentes serão implementados apenas após a validação deste ciclo.

---

## Protocolo de Recuperação

O Retriever é dirigido pelo agente.

O agente decide explicitamente qual contexto deseja recuperar.

O Context Engine nunca infere arquivos adicionais.

Exemplos:

<<RETRIEVE FILE AGENTS.md>>

<<RETRIEVE FILE bin/update_context.sh>>

<<RETRIEVE FILES
AGENTS.md
CONTEXT_SPEC.md
RETRIEVER_SPEC.md
>>

Fluxo

Agente
    │
    ▼
Solicitação RETRIEVE
    │
    ▼
Monitor
    │
    ▼
retrieve
    │
    ▼
context-builder
    │
    ▼
Conteúdo solicitado
    │
    ▼
Monitor
    │
    ▼
Agente

Princípios

- O agente controla a exploração do contexto.
- O Context Engine não toma decisões pelo agente.
- O protocolo deve ser determinístico e auditável.
- Builders executam apenas a recuperação solicitada.
- Inteligência pertence ao agente; execução pertence ao Context Engine.

