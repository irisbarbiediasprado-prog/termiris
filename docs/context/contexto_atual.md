Contexto Atual — Projeto Termiris

Visão

O objetivo atual não é refatorar a arquitetura.

O objetivo é tornar uma IA externa ("ia_chat") capaz de colaborar no desenvolvimento do Termiris utilizando exclusivamente o Termiris Protocol.

A arquitetura existente está considerada suficientemente estável para esta fase.

Toda melhoria arquitetural descoberta durante essa integração deve ser registrada no roadmap e não implementada imediatamente, salvo quando impedir o funcionamento da IA.

---

Prioridade Máxima

Ensinar a "ia_chat" a falar o dialeto Termiris.

Ela já compreendeu os conceitos de:

- Retrieve
- Builders
- Context Artifacts
- Navegação incremental

Porém ainda utiliza uma representação "natural", por exemplo:

Retriever(tree)
Retriever(current-file)

O comportamento esperado é:

<<RETRIEVE TREE>>

<<RETRIEVE CURRENT>>

<<RETRIEVE SEARCH context-builder>>

Ou seja:

O problema atual não é arquitetural.

É sintático.

---

Estado Atual

Implementado

- Object Store
- Context Builder
- Context DAG
- Garbage Collector
- Runtime
- TP Suite
- TP Certification
- Context Package
- Eventos principais do protocolo

Em andamento

- Cobertura completa dos eventos
- Ensino do protocolo para a "ia_chat"

---

Filosofia Atual

Durante esta fase é proibido:

- refatorar arquitetura
- renomear eventos
- criar V2 do protocolo
- simplificar estruturas existentes
- alterar formatos do protocolo

Essas melhorias devem apenas ser anotadas para futura refatoração.

É permitido:

- implementar eventos ainda inexistentes
- implementar handlers ausentes
- implementar builders ausentes
- implementar retrievers ausentes
- corrigir bugs do protocolo

---

Papel do TP

Os TPs não testam apenas o runtime.

Eles representam a certificação de um agente.

Exemplo:

TP-001

Verifica se o agente utiliza:

SEARCH

↓

FILE

na ordem correta.

O TP mede se a IA realmente fala o dialeto Termiris.

---

Objetivo da Fase

Atingir cobertura completa do protocolo.

Checklist simplificada:

- SEARCH
- TREE
- FILE
- CURRENT
- PROJECT_KNOWLEDGE
- RELATED_FILES
- GIT_DIFF
- ROADMAP
- TASK
- REPORT
- BUILDERS
- TP

Cada item deve possuir:

- evento implementado
- handler implementado
- documentação
- TP correspondente
- funcionamento comprovado na "ia_chat"

---

Definição de Sucesso

Uma IA recém-conectada deve ser capaz de:

1. Aprender o protocolo.
2. Solicitar contexto corretamente.
3. Navegar pelo projeto apenas através dos eventos.
4. Colaborar no desenvolvimento sem conhecer previamente o projeto.

Quando isso acontecer, o Termiris terá atingido seu primeiro MVP como protocolo para agentes.

