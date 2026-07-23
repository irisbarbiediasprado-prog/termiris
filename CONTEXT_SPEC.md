# Context Specification

Status: Draft

Version: 0.2

---

# Missão

Produzir o menor contexto possível capaz de permitir que qualquer agente execute corretamente uma tarefa.

O objetivo não é fornecer mais contexto.

O objetivo é maximizar a qualidade do contexto.

---

# Princípios

- Contexto é um artefato.
- Contexto é reproduzível.
- Contexto é atualizado.
- Contexto é modular.
- Contexto é orientado à tarefa.
- Contexto deve minimizar redundância.
- Contexto deve minimizar tokens.
- Contexto deve maximizar relevância.

Arquitetura boa não conecta componentes.

Arquitetura boa conecta artefatos.

---

# Context Engine

O Context Engine é responsável por fornecer contexto sob demanda.

Ele não decide o que a IA precisa.

Ele fornece mecanismos para que a IA descubra autonomamente o contexto necessário para executar uma tarefa.

---

# Arquitetura

Projeto
│
├── Builders
├── Processors
├── Retriever
├── Patch Engine
└── Providers

Cada componente possui responsabilidade única.

---

# Builders

Builders produzem artefatos.

Exemplos:

- current-file
- related-files
- workspace
- project-knowledge
- recent-changes
- source
- logs

Builders nunca conhecem IA.

Builders apenas produzem contexto.

---

# Processors

Processors enriquecem Builders.

Exemplos futuros:

- langextract
- git
- tree
- ripgrep
- documentação
- cache

Processors nunca alteram contratos.

---

# Retriever

O Retriever permite que agentes naveguem pelo projeto de forma incremental.

Em vez de receber todo o projeto, o agente solicita apenas o contexto necessário.

Exemplos:

retrieve(current-file)

retrieve(related-files)

retrieve(symbol:update_context)

retrieve(tree)

retrieve(git-diff)

retrieve(log)

O Retriever apenas orquestra Builders.

---

# Patch Engine

O Patch Engine permite que agentes proponham alterações estruturadas.

Exemplos:

edit(file)

apply(patch)

replace(block)

A execução pode exigir confirmação do usuário.

---

# Fluxo

Usuário

↓

Agente

↓

Retriever

↓

Builders

↓

Processors

↓

Contexto

↓

Agente

↓

Patch Engine (opcional)

↓

Projeto

---

# Qualidade de Contexto

Uma resposta nunca será melhor que o contexto que a originou.

Objetivos:

- maximizar relevância;
- minimizar tokens;
- minimizar redundância;
- manter contexto atualizado;
- preservar arquitetura.

---

# Filosofia

O Termiris não envia contexto.

O Termiris permite que agentes descubram contexto.

O agente deve aprofundar o contexto conforme a necessidade da tarefa, utilizando o Retriever para navegar pelo projeto de maneira incremental.

---

# Roadmap

v0.1

✓ Context Builder

v0.2

✓ Context Engine
- Retriever

v0.3

- Related Files
- Git
- Logs

v0.4

- LangExtract
- Knowledge Builder

v0.5

- Patch Engine

v1.0

- Agentes autônomos navegando pelo projeto através do Context Engine.

