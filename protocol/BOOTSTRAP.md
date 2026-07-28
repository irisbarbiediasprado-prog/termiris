# BOOTSTRAP Event

Status: Draft

Version: 1

---

## Objetivo

BOOTSTRAP é o primeiro evento emitido por um agente que ainda
não conhece o protocolo Termiris.

Sua finalidade é permitir que qualquer LLM aprenda
incrementalmente o protocolo utilizando o próprio protocolo.

BOOTSTRAP elimina prompts gigantes e treinamento manual.

---

## Fluxo

Agent

↓

<<BOOTSTRAP>>

↓

Runtime

↓

BOOTSTRAP Package

↓

Agent

↓

<<RETRIEVE ...>>

↓

TP Certification

↓

Agente Certificado

---

## Resposta esperada

type=BOOTSTRAP

version=1

protocol=Termiris

curriculum=TP

state=LEARNING

next=

SPEC_PROTOCOL
EVENTS
TEST_POLICY
TP_CONFORMANCE
TP_CURRICULUM

---

## Regras

BOOTSTRAP nunca envia documentos.

BOOTSTRAP apenas informa
qual é a sequência oficial de aprendizado.

O agente é responsável por solicitar
cada documento através de RETRIEVE.

---

## Sequência obrigatória

1.
<<BOOTSTRAP>>

2.
<<RETRIEVE SPEC_PROTOCOL>>

3.
<<RETRIEVE EVENTS>>

4.
<<RETRIEVE TEST_POLICY>>

5.
<<RETRIEVE TP_CONFORMANCE>>

6.
<<RETRIEVE TP_CURRICULUM>>

7.
<<TP CERTIFY>>

---

## Invariantes

BOOTSTRAP nunca contém contexto de projeto.

BOOTSTRAP nunca contém código.

BOOTSTRAP nunca contém arquitetura específica.

BOOTSTRAP apenas ensina como aprender.

---

## Resultado

Após concluir o currículo TP,
o agente torna-se compatível com o
Termiris Protocol.

