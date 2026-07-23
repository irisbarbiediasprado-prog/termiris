# Termiris Kernel

Status: Draft v0.1

## Objetivo

O Kernel é o componente responsável por mediar toda comunicação entre um agente de IA e o projeto.

A IA nunca acessa diretamente o sistema.

Toda interação ocorre através de um protocolo explícito.

---

## Loop

User

↓

LLM

↓

Kernel

↓

Syscall?

├── Não
│
└── Sim
     │
     ▼
Executa syscall

↓

Resultado

↓

LLM

↓

Resposta final

---

## Syscalls

RETRIEVE

Obtém contexto.

Exemplos:

<<RETRIEVE FILE AGENTS.md>>

<<RETRIEVE FILES
AGENTS.md
CONTEXT_SPEC.md
>>

RUN

Executa comandos autorizados.

Exemplo:

<<RUN check_ai_health>>

PATCH

Solicita alteração de arquivos.

COMMIT

Solicita criação de commit.

---

## Filosofia

A IA não manipula diretamente o projeto.

Ela apenas solicita operações.

O Kernel é responsável por:

- interpretar o protocolo;
- validar permissões;
- executar operações;
- devolver resultados.

---

## Arquitetura

            LLM
             │
             ▼
      Termiris Kernel
             │
     ┌───────┼────────┐
     ▼       ▼        ▼
 Retriever  Runner  Patch
     │       │        │
     └───────┴────────┘
             │
             ▼
          Projeto

---

## Princípios

- O Kernel implementa o protocolo.
- A IA implementa a estratégia.
- O projeto nunca é acessado diretamente pela IA.
- Toda operação é explícita.
- Toda operação é auditável.
- Toda operação pode ser reproduzida.

