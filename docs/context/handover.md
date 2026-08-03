HANDOVER — Estado Atual do Termiris

Objetivo da fase

O objetivo atual do projeto não é desenvolver novas funcionalidades nem refatorar a arquitetura.

O objetivo desta fase é transformar a "ia_chat" em um agente colaborativo, capaz de desenvolver o Termiris utilizando exclusivamente o Termiris Protocol (TP).

Toda decisão deve ser tomada considerando esse objetivo.

---

Estado da arquitetura

A infraestrutura principal já existe.

Implementado:

- Runtime
- Event Parser
- Event Bus
- Retrieve Handler
- Retrieve
- Context Builder
- Object Store baseado em SHA-256
- Garbage Collector
- Project Monitor
- Chat Monitor
- MITL
- TP Suite
- TP Certification

O gargalo não é mais a infraestrutura.

---

Arquitetura reconstruída

Após analisar os componentes implementados, o fluxo real do sistema é:

Project Monitor
        │
                ▼
                Context Builder
                        │
                        gera context.md
                                │
                                        ▼
                                        Chat Monitor
                                                │
                                                .file context.md
                                                        │
                                                                ▼
                                                                ia_chat
                                                                        │
                                                                        stdout
                                                                                ▼
                                                                                MITL
                                                                                        │
                                                                                        FIFO (.chat.pipe)
                                                                                                ▼
                                                                                                runtime
                                                                                                        │
                                                                                                                ▼
                                                                                                                event-parser
                                                                                                                        │
                                                                                                                                ▼
                                                                                                                                event-bus
                                                                                                                                        │
                                                                                                                                                ▼
                                                                                                                                                handlers
                                                                                                                                                        │
                                                                                                                                                                ▼
                                                                                                                                                                retrieve
                                                                                                                                                                        │
                                                                                                                                                                                ▼
                                                                                                                                                                                context-builder

                                                                                                                                                                                ---

                                                                                                                                                                                Responsabilidade de cada componente

                                                                                                                                                                                Project Monitor

                                                                                                                                                                                Observa alterações do projeto.

                                                                                                                                                                                Sempre que necessário produz novo contexto através do Context Builder.

                                                                                                                                                                                Não conversa diretamente com a IA.

                                                                                                                                                                                ---

                                                                                                                                                                                Context Builder

                                                                                                                                                                                Produz o contexto utilizado pela IA.

                                                                                                                                                                                Hoje produz principalmente:

                                                                                                                                                                                - context.md

                                                                                                                                                                                No futuro poderá produzir também:

                                                                                                                                                                                - contexto pedagógico
                                                                                                                                                                                - bootstrap
                                                                                                                                                                                - currículo TP

                                                                                                                                                                                sem alterar o restante da arquitetura.

                                                                                                                                                                                ---

                                                                                                                                                                                Chat Monitor

                                                                                                                                                                                É deliberadamente simples.

                                                                                                                                                                                Sua única responsabilidade é enviar contexto para a IA.

                                                                                                                                                                                Hoje faz essencialmente:

                                                                                                                                                                                .file context.md

                                                                                                                                                                                Ele:

                                                                                                                                                                                - não interpreta eventos
                                                                                                                                                                                - não conhece o protocolo
                                                                                                                                                                                - não executa comandos

                                                                                                                                                                                Essa simplicidade deve ser preservada.

                                                                                                                                                                                ---

                                                                                                                                                                                ia_chat

                                                                                                                                                                                A "ia_chat" é o agente.

                                                                                                                                                                                Ela recebe contexto através do Chat Monitor.

                                                                                                                                                                                Ela deve responder utilizando exclusivamente o Termiris Protocol.

                                                                                                                                                                                Hoje ela ainda responde parcialmente como um LLM genérico.

                                                                                                                                                                                Esse é o principal gargalo atual.

                                                                                                                                                                                ---

                                                                                                                                                                                MITL

                                                                                                                                                                                O MITL não interpreta o protocolo.

                                                                                                                                                                                Sua responsabilidade é apenas conectar a saída da "ia_chat" ao Runtime.

                                                                                                                                                                                Implementação atual:

                                                                                                                                                                                - utiliza "tmux pipe-pane"
                                                                                                                                                                                - captura todo o stdout da janela Chat
                                                                                                                                                                                - envia para um FIFO

                                                                                                                                                                                .chat.pipe

                                                                                                                                                                                que alimenta diretamente o Runtime.

                                                                                                                                                                                Portanto:

                                                                                                                                                                                MITL é apenas um adaptador de fluxo.

                                                                                                                                                                                ---

                                                                                                                                                                                Runtime

                                                                                                                                                                                O Runtime recebe tudo que a IA escreve.

                                                                                                                                                                                É responsabilidade do Runtime interpretar o protocolo.

                                                                                                                                                                                O Runtime utiliza:

                                                                                                                                                                                - Event Parser
                                                                                                                                                                                - Event Bus

                                                                                                                                                                                para transformar texto em eventos estruturados.

                                                                                                                                                                                ---

                                                                                                                                                                                Event Parser

                                                                                                                                                                                Transforma eventos textuais em eventos estruturados.

                                                                                                                                                                                Exemplo esperado:

                                                                                                                                                                                <<RETRIEVE SEARCH context-builder>>

                                                                                                                                                                                ↓

                                                                                                                                                                                Evento interno.

                                                                                                                                                                                ---

                                                                                                                                                                                Event Bus

                                                                                                                                                                                Despacha o evento para os handlers.

                                                                                                                                                                                ---

                                                                                                                                                                                Retrieve Handler

                                                                                                                                                                                Executa eventos RETRIEVE.

                                                                                                                                                                                ---

                                                                                                                                                                                Bootstrap

                                                                                                                                                                                O projeto já possui um documento BOOTSTRAP.

                                                                                                                                                                                O documento está correto.

                                                                                                                                                                                Ele descreve a sequência oficial de aprendizado:

                                                                                                                                                                                BOOTSTRAP

                                                                                                                                                                                ↓

                                                                                                                                                                                SPEC_PROTOCOL

                                                                                                                                                                                ↓

                                                                                                                                                                                EVENTS

                                                                                                                                                                                ↓

                                                                                                                                                                                TEST_POLICY

                                                                                                                                                                                ↓

                                                                                                                                                                                TP_CONFORMANCE

                                                                                                                                                                                ↓

                                                                                                                                                                                TP_CURRICULUM

                                                                                                                                                                                ↓

                                                                                                                                                                                TP CERTIFY

                                                                                                                                                                                Não é necessário criar um novo bootstrap.

                                                                                                                                                                                ---

                                                                                                                                                                                Estado do aprendizado da IA

                                                                                                                                                                                Hoje a IA compreende conceitualmente o sistema.

                                                                                                                                                                                Exemplo observado:

                                                                                                                                                                                Retriever(tree)

                                                                                                                                                                                Entretanto ela ainda não fala o dialeto oficial.

                                                                                                                                                                                O esperado é:

                                                                                                                                                                                <<RETRIEVE TREE>>

                                                                                                                                                                                Portanto o problema atual não é conhecimento.

                                                                                                                                                                                É linguagem.

                                                                                                                                                                                ---

                                                                                                                                                                                Principal descoberta

                                                                                                                                                                                A arquitetura já suporta completamente um agente baseado em protocolo.

                                                                                                                                                                                Não é necessário:

                                                                                                                                                                                - criar novos monitores
                                                                                                                                                                                - criar um executor de bootstrap
                                                                                                                                                                                - modificar o MITL
                                                                                                                                                                                - modificar o Runtime

                                                                                                                                                                                A infraestrutura necessária já existe.

                                                                                                                                                                                ---

                                                                                                                                                                                Próxima direção

                                                                                                                                                                                O esforço deve concentrar-se exclusivamente em ensinar a "ia_chat" a utilizar corretamente o Termiris Protocol.

                                                                                                                                                                                Isso significa:

                                                                                                                                                                                - aprender a emitir eventos TP
                                                                                                                                                                                - aprender a solicitar contexto
                                                                                                                                                                                - aprender a seguir o currículo TP
                                                                                                                                                                                - abandonar respostas livres quando o protocolo exigir eventos

                                                                                                                                                                                ---

                                                                                                                                                                                TP

                                                                                                                                                                                Os TPs passam a representar a certificação do agente.

                                                                                                                                                                                Exemplo:

                                                                                                                                                                                TP-001

                                                                                                                                                                                verifica se o agente inicia corretamente com:

                                                                                                                                                                                <<RETRIEVE SEARCH context-builder>>

                                                                                                                                                                                em vez de:

                                                                                                                                                                                Retriever(tree)

                                                                                                                                                                                Cada TP aprovado representa uma habilidade adquirida.

                                                                                                                                                                                ---

                                                                                                                                                                                Estratégia da fase

                                                                                                                                                                                Sempre que houver dúvida:

                                                                                                                                                                                Não modificar a arquitetura.

                                                                                                                                                                                Perguntar primeiro:

                                                                                                                                                                                "A IA sabe fazer isso utilizando o protocolo?"

                                                                                                                                                                                Se:

                                                                                                                                                                                NÃO

                                                                                                                                                                                ↓

                                                                                                                                                                                ensinar a IA.

                                                                                                                                                                                Se:

                                                                                                                                                                                SIM

                                                                                                                                                                                ↓

                                                                                                                                                                                verificar Runtime.

                                                                                                                                                                                Somente implementar infraestrutura quando o Runtime realmente não suportar um evento previsto no protocolo.

                                                                                                                                                                                ---

                                                                                                                                                                                Critério de sucesso

                                                                                                                                                                                Esta fase será concluída quando uma nova instância da "ia_chat" conseguir:

                                                                                                                                                                                1. iniciar pelo BOOTSTRAP;
                                                                                                                                                                                2. aprender utilizando apenas os documentos oficiais;
                                                                                                                                                                                3. emitir corretamente os eventos TP;
                                                                                                                                                                                4. ser aprovada nos testes TP;
                                                                                                                                                                                5. colaborar no desenvolvimento do Termiris utilizando exclusivamente o Termiris Protocol.

                                                                                                                                                                                Neste momento, o foco principal do projeto deixa de ser infraestrutura e passa a ser alfabetização do agente.

