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
