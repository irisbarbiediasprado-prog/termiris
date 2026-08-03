
Eu não implementaria learning dentro do context-builder.
Depois de entender a arquitetura, acho que isso mistura responsabilidades.
Hoje o context-builder já tem uma responsabilidade muito clara:
construir objetos de contexto;
fazer merge;
armazenar;
fazer GC.
Ele é praticamente um Git de contexto.
Se colocarmos:
context-builder learning
ele passa a conhecer pedagogia, TP, bootstrap... e isso quebra a separação que vocês construíram.
O que eu implementaria
Eu criaria um Builder.
Algo como:
bin/bootstrap-builder
ou
bin/learning-builder
Responsabilidade única:
BOOTSTRAP
        │
                ▼
                gera context.md
                Assim o fluxo fica bonito:
                Project Monitor
                        │
                                ├──────────────┐
                                        ▼              ▼
                                        context-builder   bootstrap-builder
                                                │              │
                                                        └──────┬───────┘
                                                                       ▼
                                                                                 context.md
                                                                                                ▼
                                                                                                         Chat Monitor
                                                                                                                        ▼
                                                                                                                                    ia_chat
                                                                                                                                    O context-builder continua sem saber que existe IA.
                                                                                                                                    O bootstrap-builder sabe apenas construir contexto pedagógico.
                                                                                                                                    Se eu tivesse que implementar uma única coisa agora
                                                                                                                                    Seria:
                                                                                                                                    bin/bootstrap-builder
                                                                                                                                    Com uma saída fixa, por exemplo:
                                                                                                                                    # Agent Bootstrap

                                                                                                                                    State

                                                                                                                                    LEARNING

                                                                                                                                    Current lesson

                                                                                                                                    BOOTSTRAP

                                                                                                                                    Expected action

                                                                                                                                    <<BOOTSTRAP>>
                                                                                                                                    Nada de lógica.
                                                                                                                                    Nada de estado.
                                                                                                                                    Nada de currículo.
                                                                                                                                    Só provar que conseguimos trocar o contexto enviado para a IA sem tocar em nenhuma outra peça.
                                                                                                                                    Essa é a implementação que eu faria primeiro. Ela preserva completamente a arquitetura existente e mantém cada Builder com uma única responsabilidade. Quando funcionar, o bootstrap-builder pode evoluir naturalmente para gerar as próximas lições do currículo TP, sem contaminar o context-builder com responsabilidades pedagógicas.

