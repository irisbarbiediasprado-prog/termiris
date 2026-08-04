# Termiris Protocol (TP)

Status: Consolidated
Version: 0.2
Author: Termiris
Content-Type: text/plain

---

# 1. Objetivo

O Termiris Protocol (TP) define como um agente conversa com o ambiente
Termiris.

Todo comando deve ser:

- determinístico;
- idempotente quando possível;
- legível por humanos;
- legível por máquinas.

O protocolo é orientado a texto puro.

---

# 2. Estrutura

Um comando possui a forma:

<<VERB TARGET ARGUMENTS...>>

---

# 3. Respostas

Formato:

BEGIN <TYPE>

STATUS: OK | ERROR

...

END <TYPE>

---

# 4. STATUS

STATUS: OK - operação executada.

STATUS: ERROR - operação falhou. Quando ERROR, campo ERROR é obrigatório.

---

# 5. ERROR

Códigos definidos:

FILE_NOT_FOUND
DIRECTORY_NOT_FOUND
INVALID_ARGUMENT
EMPTY_RESULT
PERMISSION_DENIED
NOT_IMPLEMENTED
INTERNAL_ERROR
BACKEND_NOT_FOUND

Princípio: erros de domínio devem ser tipados e pertencentes ao protocolo,
nunca ValueError genérico. Em particular, a resolução de um backend
inexistente deve produzir um erro tipado do domínio do protocolo.

---

# 6. Backend Contract

Todo backend deve expor duas fases distintas:

validate(plan) -> None
  Verifica estrutura do plano. Não produz efeitos colaterais.

compile(plan) -> List[Operation]
  Tradução pura: plano semântico para operações primitivas.
  Deve permanecer livre de efeitos colaterais, sem acesso a filesystem,
  sem IO, sem execução.

A execução é responsabilidade exclusiva do Runtime.

---

# 7. RETRIEVE

Família de obtenção de informações.

- FILE: solicita arquivos
- TREE: retorna árvore de diretório
- SEARCH: pesquisa por texto
- DIFF: diferenças
- STATUS: estado do projeto

SEARCH faz parte da linguagem do protocolo, mas sua implementação
está marcada como adiada para v0.3. Isso separa linguagem suportada
de estado da implementação.

---

# 8. Compatibilidade

Novos comandos nunca alteram sintaxe existente.

Novas funcionalidades como novos VERBs ou TARGETs.

Quebras de API pública só após rg confirmar 0 consumidores e testes verdes.

---

# 9. Futuro

VERBs planejados: PATCH, RUN, TEST, COMMIT, PLAN, APPLY

RETRIEVE SEARCH - implementação após base v0.2 estável.

---

# 10. Pureza das Camadas

Nenhuma etapa anterior pode executar responsabilidades de etapas posteriores.

Em particular:

- Plugins não executam IO.
- Compilers não acessam o filesystem.
- Backends não executam operações durante compile().
- Runtime é o único responsável por materializar efeitos colaterais.

Este princípio resume as fronteiras arquiteturais descobertas no v0.2
e orienta novos contribuidores sobre onde cada responsabilidade pertence.
