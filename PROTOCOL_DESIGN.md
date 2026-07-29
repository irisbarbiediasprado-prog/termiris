# Protocol Design

## Filosofia

O protocolo do Termiris não é transportado por um stream de bytes.

Ele é transportado pela tela.

Essa diferença é fundamental.

O MITL não interpreta ANSI, não interpreta comandos, não interpreta protocolo.

Sua única responsabilidade é reconstruir exatamente o que um usuário enxergaria em um terminal.

```
PTY
        │
        ▼
Terminal Emulator
        │
        ▼
Virtual Screen
```

O ProtocolExtractor trabalha exclusivamente sobre essa tela virtual.

```
Virtual Screen
        │
        ▼
ProtocolExtractor
        │
        ▼
Socket
```

## Por que não usar o stream?

Streams possuem propriedades que tornam a interpretação de protocolos extremamente frágil.

Exemplos:

- fragmentação de pacotes
- redraw do terminal
- sequências ANSI
- scroll
- atualizações parciais
- repaint
- mudanças de cursor

Todos esses eventos aparecem naturalmente em um terminal moderno.

Nenhum deles representa intenção do usuário.

Logo, eles não pertencem ao protocolo.

## A tela é a fonte da verdade

Depois que o TerminalEmulator termina seu trabalho existe apenas um estado.

Exemplo:

Durante a renderização o stream pode conter

```
ESC[31m
ESC[2K
cursor left
cursor right
redraw
<<RETR
IEVE FILE
README.md>>
```

Depois da renderização existe somente

```
<<RETRIEVE FILE README.md>>
```

É exatamente isso que interessa ao ProtocolExtractor.

## Separação de responsabilidades

MITL

- captura PTY
- emula terminal
- produz tela virtual

ProtocolExtractor

- procura tags
- elimina duplicações
- publica eventos

event-parser

- interpreta protocolo
- produz operações

Runtime

- executa operações

Chat

- apenas consome snapshots

## Regra arquitetural

Nenhuma camada conhece a implementação da camada seguinte.

MITL não conhece Runtime.

Runtime não conhece PTY.

Chat não conhece arquivos.

Cada componente conversa apenas com sua interface imediatamente inferior.

## Consequências

Essa arquitetura torna o protocolo independente de

- ANSI
- terminal utilizado
- modelo de IA
- parser
- transporte
- socket
- PTY

O protocolo existe apenas como informação visível na tela.

Todo o restante é detalhe de implementação.
