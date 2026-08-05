# Retriever Specification

**Status:** Draft  
**Version:** 0.2

---

# Missão

Permitir que agentes descubram conhecimento incrementalmente.

O Retriever não produz conhecimento.

O Retriever apenas resolve recursos solicitados pelo agente e retorna um `Artifact`.

O agente controla a exploração.

O Runtime executa a recuperação.

---

# Objetivos

- Recuperação incremental.
- Responsabilidade única.
- Operações determinísticas.
- Baixo custo.
- Baixa latência.
- Artefatos reproduzíveis.
- Nenhum contexto implícito.

O agente nunca recebe "o projeto inteiro".

O agente descobre apenas o que precisa.

---

# Pipeline

```
Agent
    ↓
RETRIEVE
    ↓
Intent
    ↓
Compiler
    ↓
MigrationPlan
    ↓
Backend
    ↓
ISA
    ↓
RetrieveExecutor
    ↓
RetrieveProvider
    ↓
Artifact
```

O pipeline é o mesmo para qualquer tipo de recuperação.

Apenas o `RetrieveProvider` muda.

---

# Contrato

Todo `RETRIEVE` retorna exatamente um `Artifact`.

```python
Artifact(
    uri: str,
    content: str,
    metadata: dict,
)
```

O Runtime nunca retorna:

- strings
- listas
- dicts especiais
- objetos diferentes

Todo recurso recuperado é representado como um `Artifact`.

---

# Resource Providers

Cada tipo de recurso possui exatamente um Provider responsável.

Exemplos:

- FileProvider
- StatusProvider
- AnalysisProvider
- HandoverProvider
- KnowledgeProvider
- GitProvider
- SymbolProvider

Providers possuem responsabilidade única.

Eles apenas resolvem recursos.

Não interpretam protocolo.

Não conversam com a IA.

---

# Resource Types

## FILE

Comando

```text
<<RETRIEVE FILE path>>
```

URI

```text
file://path
```

Origem

- Filesystem

Persistência

- Sim

Provider

- FileProvider

---

## STATUS

Comando

```text
<<RETRIEVE STATUS>>
```

URI

```text
status://current
```

Origem

- Runtime
- Snapshot
- Registries

Persistência

- Não

Provider

- StatusProvider

O conteúdo é derivado do estado atual do Runtime.

---

## ANALYSIS

Comando

```text
<<RETRIEVE ANALYSIS>>
```

URI

```text
analysis://architecture
```

Origem

- Artifact de análise

Persistência

- Sim

Provider

- AnalysisProvider

Caso ainda não exista, retorna um Artifact vazio.

---

## HANDOVER

Comando

```text
<<RETRIEVE HANDOVER>>
```

URI

```text
handover://current
```

Origem

- STATUS
- ANALYSIS
- Overview do projeto

Persistência

- Não

Provider

- HandoverProvider

O conteúdo é composto sob demanda.

Nunca é armazenado.

---

## TREE

Comando

```text
<<RETRIEVE TREE>>
```

URI

```text
tree://workspace
```

Origem

- Filesystem

Provider

- TreeProvider

---

## SYMBOL

Comando

```text
<<RETRIEVE SYMBOL update_context>>
```

URI

```text
symbol://update_context
```

Origem

- Índice do projeto

Provider

- SymbolProvider

---

## KNOWLEDGE

Comando

```text
<<RETRIEVE KNOWLEDGE>>
```

Origem

Artefatos persistentes do projeto.

Exemplos:

- AGENTS.md
- README.md
- SPECs
- documentação

Provider

- KnowledgeProvider

---

## GIT

Comandos

```text
<<RETRIEVE GIT STATUS>>

<<RETRIEVE GIT DIFF>>

<<RETRIEVE GIT COMMITS>>
```

Provider

- GitProvider

---

## LOGS

Comandos

```text
<<RETRIEVE LOG>>

<<RETRIEVE HISTORY>>

<<RETRIEVE DIAGNOSTICS>>
```

Provider

- LogProvider

---

# Princípios

- O agente controla a exploração.
- O Retriever nunca infere recursos adicionais.
- O Runtime não possui caminhos especiais.
- Cada Provider resolve apenas seu recurso.
- Inteligência pertence ao agente.
- Execução pertence ao Runtime.
- Todo resultado é um Artifact.

---

# Não Objetivos

O Retriever nunca:

- conversa com a IA;
- interpreta respostas;
- modifica arquivos;
- aplica patches;
- toma decisões arquiteturais;
- gera código.

Seu papel é apenas recuperar recursos.

---

# Evolução

Novos recursos são adicionados registrando novos Providers.

Exemplos futuros:

- workspace://
- decision://
- metrics://
- history://
- snapshot://
- protocol://

Nenhuma alteração no Runtime ou no pipeline principal deve ser necessária.

---

# Milestones

## Milestone 1

Validar recuperação incremental de arquivos.

Implementado:

- FILE

---

## Milestone 2

Validar recuperação incremental de conhecimento.

Implementar:

- STATUS
- ANALYSIS
- HANDOVER

Critério de sucesso:

Um agente consegue compreender o estado do projeto solicitando apenas os recursos necessários.

---

# Filosofia

O contexto deixa de ser enviado.

O contexto passa a ser descoberto.

O Retriever não sabe o que é importante.

Ele apenas resolve recursos.

A inteligência permanece no agente.
