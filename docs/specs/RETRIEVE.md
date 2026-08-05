Retrieve Protocol

Status: Draft
Versão: 0.2

Objetivo

O comando "RETRIEVE" é a capacidade universal de recuperação de conhecimento do Termiris.

Seu objetivo é transformar diferentes tipos de recursos em um "Artifact" padronizado.

Todo "RETRIEVE" produz exatamente um "Artifact".

---

Pipeline

RETRIEVE
    ↓
Plugin
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
Resource Handler
    ↓
Artifact

O fluxo utiliza a arquitetura normal do protocolo.

Não existe caminho especial no Runtime ou Dispatcher.

---

Contrato

Todo recurso recuperado deve retornar:

Artifact(
    uri: str,
    content: str,
    metadata: dict,
)

O executor nunca retorna diretamente:

- "str"
- "list"
- "dict"
- objetos específicos de implementação

A fronteira do Runtime é sempre um "Artifact".

---

Intent

"RETRIEVE" não representa um "IntentKind" único.

A intenção depende da natureza do recurso.

Exemplos:

RETRIEVE FILE
        ↓
READ_RESOURCE

RETRIEVE STATUS
        ↓
QUERY_STATE

O comando descreve a capacidade desejada.

A Intent descreve a semântica.

---

Recursos

FILE

URI:

file://...

Origem:

Filesystem

Semântica:

Recuperação de conteúdo persistente.

Exemplo:

<<RETRIEVE FILE main.py>>

Resultado:

Artifact(
    uri="file://main.py"
)

Persistência:

Sim

---

STATUS

URI:

status://current

Origem:

Runtime
Snapshot
Registries
State

Semântica:

Recuperação do estado atual do sistema.

Exemplo:

<<RETRIEVE STATUS>>

Resultado:

Artifact(
    uri="status://current"
)

Persistência:

Não

O conteúdo é derivado do estado atual do Runtime.

---

ANALYSIS

URI:

analysis://architecture

Origem:

Knowledge Artifacts

Semântica:

Recuperação de análises persistidas.

Persistência:

Sim

Caso não exista:

Retorna um "Artifact" vazio válido.

---

HANDOVER

URI:

handover://current

Origem:

STATUS
ANALYSIS
Overview

Semântica:

Representa uma visão consolidada para continuidade de contexto.

Persistência:

Não

É derivado do estado atual.

---

Resource Handler

Cada tipo de recurso possui um resolvedor responsável.

Responsabilidades:

- localizar o recurso;
- gerar conteúdo;
- construir metadata;
- retornar Artifact.

Não conhece:

- protocolo;
- Intent;
- ISA;
- Compiler.

---

Regras

1. Todo "RETRIEVE" retorna exatamente um "Artifact".
2. O Runtime não possui caminhos especiais para RETRIEVE.
3. Plugins nunca executam recuperação diretamente.
4. Backend nunca acessa recursos.
5. Resource Handlers não conhecem o protocolo.
6. ISA apenas representa a operação de execução.
7. A recuperação é sempre convertida em Artifact.

---

Fora do escopo

Não faz parte desta versão:

- escrita ("MUTATE_*");
- provenance;
- versionamento;
- histórico de decisões;
- Construction Pipeline;
- cache de recursos.

---

Evolução

Novos recursos devem ser adicionados através de novos handlers.

Exemplos futuros:

history://
decision://
workspace://
metrics://
context://

A expansão deve adicionar capacidade, não novos caminhos arquiteturais.

---

Decisões rejeitadas

RetrieveBackend separado

Rejeitado.

Motivo:

RETRIEVE é uma operação ISA, não um backend.

---

RetrievePlugin gerando Operation

Rejeitado.

Motivo:

O plugin não deve conhecer ISA nem Runtime.

---

QueryCompiler separado

Rejeitado.

Motivo:

RETRIEVE não cria uma família nova de compiladores.

A semântica continua sendo expressa através de Intent existente.

---

Provider como camada obrigatória

Rejeitado neste momento.

Motivo:

Criaria uma abstração antes da necessidade real.

A implementação atual usa Resource Handlers.

Uma camada Provider poderá existir futuramente caso múltiplos handlers precisem de composição ou descoberta dinâmica.

---

Estado atual

Implementado:

PrimitiveISA.RETRIEVE
RetrieveExecutor
STATUS handler
FILE handler

Testado:

RETRIEVE STATUS pipeline
RETRIEVE STATUS runtime
suíte completa

Resultado:

Pipeline único preservado.
