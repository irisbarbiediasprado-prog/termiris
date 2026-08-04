# Termiris Architecture

## Pipeline

Text
→ Tokenizer
→ AST
→ Intent
→ IntentCompiler
→ MigrationPlan
→ Backend
→ Operation
→ Executor
→ Runtime

---

## Core Principles

The protocol layer is semantic.
The runtime layer is operational.
The backend is the only translation boundary.

---

## Architectural Invariants

1. IntentCompiler produces MigrationPlan.
2. MigrationPlan is backend-agnostic.
3. Only ISABackend translates MigrationPlan into Operation.

4. **Artifact is unique.** Executors never create new Artifact subtypes. Rich structures are serialized into `content` (str) and preserved in `metadata` (dict). The domain model remains singular; only representation varies.


4. Runtime executes Operation without knowing Intent.
5. Backend implementations are resolved through BackendRegistry.
6. Executor implementations are resolved through ExecutorRegistry.
7. New protocols extend the system by registering compilers.
8. New backends extend the system by registering backends.
9. New executors extend the system by registering executors.

---

## Dependency Direction

Text
    ↓
Intent
    ↓
MigrationPlan
    ↓
Backend
    ↓
Operation
    ↓
Executor
    ↓
Runtime

Dependencies must always point downward.

Regra de Ouro

Se um novo protocolo exigir modificar:

- ProtocolCompiler
- RuntimeEngine
- Dispatcher
- BackendRegistry
- ExecutorRegistry

a arquitetura está regredindo.

O correto é adicionar:

- um IntentCompiler
- um Backend
- um Executor

e registrar os componentes.
