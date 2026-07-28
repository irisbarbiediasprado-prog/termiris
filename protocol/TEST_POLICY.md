# Termiris Test Policy

## Objetivo

Definir a política oficial de testes do Termiris.

O projeto possui duas camadas independentes de validação:

- Protocol Suite (TP)
- Runtime Suite

Essas camadas possuem responsabilidades diferentes e nunca devem ser misturadas.

---

# 1. Protocol Suite (TP)

Objetivo

Validar o contrato entre o Agente e a Engine.

Escopo

- Estratégia do agente
- Ordem dos eventos
- Uso correto do protocolo
- SEARCH
- FILE
- RETRIEVE
- TP_RESULT
- Restrições do protocolo
- Critérios de conformidade

Os TPs são independentes da implementação.

Um TP continua válido mesmo que toda a engine seja reescrita.

Diretório

protocol/tests/

Runner

bin/tp-suite

---

# 2. Runtime Suite

Objetivo

Validar a implementação da engine.

Escopo

- parser
- event-bus
- runtime
- handlers
- context-store
- replay
- merge
- gc
- metrics
- reports
- notifications

Mudanças internas da engine podem alterar estes testes.

Diretório

bin/check-*

Runner

bin/runtime-suite

---

# Separação de responsabilidades

Protocol Suite responde:

"O agente falou corretamente?"

Runtime Suite responde:

"A engine executou corretamente?"

Jamais utilizar um TP para validar detalhes internos da implementação.

Jamais utilizar um Runtime Test para validar comportamento do protocolo.

---

# Fluxo oficial de implementação

Toda funcionalidade nova deve seguir exatamente esta ordem:

1.
Especificar o comportamento.

- Criar ou atualizar documentação.
- Caso altere o protocolo, criar TP.

2.
Criar o teste.

- Runtime → bin/check-*
- Protocolo → protocol/tests/TP-XXX.md

3.
Executar.

O teste deve falhar inicialmente.

4.
Implementar.

Preferencialmente utilizando um único cat >.

5.
Executar novamente.

O teste deve passar.

6.
Registrar.

Adicionar ao runner correspondente.

7.
Commit.

Nunca implementar primeiro para escrever o teste depois.

---

# Critério arquitetural

Protocol Suite define o contrato público.

Runtime Suite define a implementação.

A implementação pode evoluir livremente.

O protocolo deve permanecer estável.

