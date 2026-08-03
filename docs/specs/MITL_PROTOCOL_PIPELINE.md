# MITL Protocol Pipeline

## Visão Geral

O MITL é responsável por transformar a saída visual do terminal em eventos estruturados do protocolo Termiris.

Cada componente possui uma única responsabilidade.

```
PTY
 │
 ▼
TerminalEmulator
 │
 ▼
ProtocolExtractor
 │
 ▼
SocketServer
 │
 ▼
event-parser
 │
 ▼
ProtocolRuntime
 │
 ▼
Protocol Plugins
```

---

## 1. PTY

Responsável apenas por executar o processo filho.

Produz um fluxo contínuo de bytes contendo:

- texto
- sequências ANSI
- movimentação de cursor
- repaint
- cores

Não conhece o protocolo.

---

## 2. TerminalEmulator

Recebe o fluxo bruto do PTY.

Responsabilidades:

- interpretar ANSI/CSI
- atualizar o estado lógico da tela
- manter o framebuffer textual

Não conhece o protocolo.

Entrada:

```
bytes
```

Saída:

```
estado lógico da tela
```

---

## 3. ProtocolExtractor

Analisa exclusivamente a tela lógica.

Responsabilidades:

- localizar tags

```
<<...>>
```

- eliminar duplicatas
- emitir apenas eventos completos

Não conhece sockets nem runtime.

Entrada:

```
texto renderizado
```

Saída:

```
<<RETRIEVE ...>>
<<PATCH ...>>
...
```

---

## 4. SocketServer

Transporta eventos.

Responsabilidades:

- multiplexar clientes
- enviar uma tag completa por evento

Nunca envia bytes do terminal.

Nunca interpreta protocolo.

---

## 5. event-parser

Consumidor de eventos.

Responsabilidades:

- receber uma tag
- chamar ProtocolRuntime

Não interpreta ANSI.

Não reconstrói streams.

Não procura delimitadores.

---

## 6. ProtocolRuntime

Traduz comandos do protocolo em operações.

Fluxo:

```
Tag

↓

AST

↓

Intent

↓

Operation

↓

Plugin
```

O Runtime nunca conhece PTY nem TerminalEmulator.

---

# Princípios Arquiteturais

## Separação de responsabilidades

PTY
→ produz bytes

TerminalEmulator
→ interpreta terminal

ProtocolExtractor
→ detecta protocolo

SocketServer
→ transporta eventos

event-parser
→ despacha

ProtocolRuntime
→ executa protocolo

Plugins
→ implementam funcionalidades

---

## Regra Fundamental

Cada camada conhece apenas a camada imediatamente seguinte.

Nenhuma camada deve assumir responsabilidades das demais.

---

## Benefícios

- parser determinístico
- protocolo independente do terminal
- transporte desacoplado
- fácil instrumentação
- novos VERBs não exigem alterações no MITL
- arquitetura orientada a eventos
