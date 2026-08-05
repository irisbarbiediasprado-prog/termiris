1. Objetivo

Adicionar suporte ao comando "RETRIEVE" dentro da arquitetura existente do Termiris, permitindo recuperar informações através do mesmo fluxo utilizado pelos demais comandos:

Entrada textual
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
PrimitiveISA Operation
    ↓
Executor
    ↓
Artifact

O objetivo principal foi evitar criar um caminho paralelo para consultas, mantendo a filosofia:

«Intenções geram planos; planos geram operações; operações são executadas pelo runtime.»

---

2. Implementação final

Fluxo implementado

Exemplo:

<<RETRIEVE STATUS>>

Fluxo:

Tokenizer
    ↓
CommandRouter.auto_discover()
    ↓
RetrievePlugin
    ↓
Intent(
    kind=QUERY_STATE,
    target="status://current"
)
    ↓
QueryStateCompiler
    ↓
MigrationPlan(
    action="RETRIEVE",
    provider="STATUS"
)
    ↓
ISABackend
    ↓
Operation(
    instruction=PrimitiveISA.RETRIEVE,
    payload={
        provider:"STATUS",
        target:"status://current"
    }
)
    ↓
RetrieveExecutor
    ↓
Artifact(
    uri="status://current"
)

---

3. Componentes adicionados ou alterados

Intent Layer

O "IntentKind" foi expandido para permitir consultas estruturadas.

Responsabilidade:

- representar intenção sem conhecer execução;
- não saber sobre arquivos, runtime ou ISA.

Exemplo:

Intent(
    kind=IntentKind.QUERY_STATE,
    target="status://current"
)

---

RetrievePlugin

Local:

lib/protocol/plugins/retrieve/__init__.py

Responsabilidade:

- interpretar:

<<RETRIEVE STATUS>>
<<RETRIEVE FILE main.py>>
<<RETRIEVE TREE lib>>

- transformar AST em Intent.

Não executa nada.

---

Compiler

Local:

lib/protocol/compiler.py

Adicionado:

QueryStateCompiler

Responsabilidade:

Converter:

Intent(QUERY_STATE)

em:

MigrationPlan(RETRIEVE)

Exemplo:

MigrationStep(
    action="RETRIEVE",
    parameters={
        "provider":"STATUS"
    }
)

---

Backend

Local:

lib/protocol/isa_backend.py

Responsabilidade:

Traduzir:

MigrationStep(RETRIEVE)

para:

Operation(
    PrimitiveISA.RETRIEVE
)

O backend não conhece:

- arquivos;
- status;
- runtime;
- providers.

Ele apenas traduz semântica para ISA.

---

RetrieveExecutor

Local:

lib/runtime/retrieve_executor.py

Responsabilidade:

Executar providers.

Providers atuais:

STATUS
ANALYSIS
HANDOVER
FILE

Exemplo:

provider="STATUS"

gera:

Artifact(
 uri="status://current"
)

---

4. Testes adicionados

Teste de pipeline

Valida:

texto
 ↓
plugin
 ↓
intent
 ↓
compiler
 ↓
backend
 ↓
operation

Arquivo:

tests/test_retrieve_status.py

Resultado:

✅ RETRIEVE STATUS pipeline OK

---

Teste de runtime

Valida:

Operation
 ↓
ExecutorRegistry
 ↓
RetrieveExecutor
 ↓
Artifact

Arquivo:

tests/test_retrieve_runtime.py

Resultado:

✅ RETRIEVE STATUS runtime OK

---

Suíte completa

Resultado:

✅ todos os testes passando

---

5. Problemas encontrados durante implementação

5.1 Metadata incompatível

Problema:

O plugin novo retornava:

{
 "resource_type":"FILE",
 "targets":["main.py"]
}

Mas o compiler existente esperava:

{
 "sub_type":"FILE",
 "targets_list":["main.py"]
}

Correção:

Manter compatibilidade adicionando os campos esperados.

Decisão:

Não quebrar contratos existentes.

---

5.2 Router vazio nos testes

Problema:

O teste criava:

router = CommandRouter()

mas não chamava:

router.auto_discover()

Resultado:

Comando RETRIEVE não reconhecido

Correção:

O teste passou a usar o mesmo fluxo real de descoberta.

---

5.3 ExecutorRegistry incompleto

Problema:

O caminho:

create_executor_registry(None)

retornava apenas:

"default": ISAExecutor()

e ignorava:

PrimitiveISA.RETRIEVE

Correção:

Registrar RETRIEVE também no caminho de compatibilidade.

---

6. Alternativas rejeitadas

Alternativa 1 — Criar QueryCompiler separado

Proposta inicial:

QueryCompiler
    ↓
MigrationPlan

com um módulo separado:

lib/protocol/query_compiler.py

Motivo da rejeição

Criaria uma segunda abstração paralela:

Compiler
    ├── BuildCompiler
    ├── SearchCompiler
    └── QueryCompiler

sem necessidade.

O sistema já possui:

IntentKind
    ↓
CompilerRegistry

Portanto a solução escolhida foi:

IntentKind.QUERY_STATE
    ↓
QueryStateCompiler

dentro do compiler existente.

---

Alternativa 2 — RetrievePlugin gerar Operation diretamente

Fluxo rejeitado:

Plugin
 ↓
Operation
 ↓
Executor

Motivo:

Quebra a arquitetura.

O plugin passaria a conhecer:

- PrimitiveISA;
- payload;
- runtime.

Problema:

Uma mudança no runtime exigiria alterar plugins.

---

Alternativa 3 — Criar RetrieveBackend separado

Fluxo rejeitado:

Intent
 ↓
RetrieveBackend
 ↓
Executor

Motivo:

Criaria um backend especializado para apenas um comando.

A arquitetura atual já suporta:

MigrationPlan
 ↓
Backend

O RETRIEVE é apenas uma nova operação.

---

Alternativa 4 — Criar caminho especial no dispatcher

Exemplo rejeitado:

if command == "RETRIEVE":
    execute_special_case()

Motivo:

Seria uma exceção arquitetural.

Todos os comandos devem seguir:

Plugin → Intent → Plan → Backend → ISA → Executor

---

7. Estado arquitetural após implementação

Antes:

READ
SEARCH
BUILD
LIST
SNAPSHOT

Depois:

READ
SEARCH
BUILD
LIST
SNAPSHOT
RETRIEVE

Sem novos caminhos.

---

8. Próximas extensões naturais

Agora novos providers podem ser adicionados sem alterar o pipeline:

Exemplo:

RETRIEVE LOGS
RETRIEVE METRICS
RETRIEVE CONTEXT
RETRIEVE MEMORY

A expansão fica limitada ao executor:

_PROVIDER = {
    STATUS: handler,
    ANALYSIS: handler,
    HANDOVER: handler,
    NOVO_PROVIDER: handler
}

---

9. Conclusão

A implementação confirmou a arquitetura proposta:

- Intent continua semântica.
- Compiler continua responsável por planejamento.
- Backend continua traduzindo para ISA.
- Executor continua responsável por efeitos reais.
- Plugins continuam independentes.

O RETRIEVE entrou como uma capacidade nativa do protocolo, não como uma exceção.
