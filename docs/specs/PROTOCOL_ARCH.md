# 🔌 Documentação Arquitetural: Termiris VPM & Framework de Plugins
A **Virtual Protocol Machine (VPM)** do Termiris é uma infraestrutura desacoplada, declarativa e extensível, projetada para compilar instruções emitidas por modelos de Linguagem (LLMs) em instruções primitivas de uma **ISA (Instruction Set Architecture)**.
O ecossistema adota o princípio **Open/Closed**: novas capacidades e comandos são adicionados via **Plugins autocontidos**, sem a necessidade de modificar o núcleo do sistema (Kernel, Parser ou Router).
## 🏛️ 1. O Fluxo de Compilação (Pipeline em 3 Estágios)
Quando uma instrução como << RETRIEVE FILE main.py >> é emitida, ela passa por um pipeline estrito inspirado na arquitetura de compiladores modernos:
```text
       [ Input Bruto ] (ex: << RETRIEVE FILE main.py >>)
              │
              ▼
       [ Tokenizer ] ──> Extrai os tokens internos
              │
              ▼
     [ CommandRouter ] ──> Localiza o Plugin via Auto-Discovery
              │
              ▼
 ┌─────────────────────────────────────────────────────────┐
 │                      PLUGIN PIPELINE                    │
 │                                                         │
 │  1. parse_ast()         ──> Sintaxe  (AST)              │
 │  2. lower_to_intent()   ──> Semântica (IR / Intenção)   │
 │  3. lower_to_operations() ──> Compilação para ISA       │
 └─────────────────────────────────────────────────────────┘
              │
              ▼
     [ Lista de Operations ] (Instruções Primitivas da ISA)
              │
              ▼
     [ Runtime Engine ] (Execução Final no Ambiente)

```
## 🧱 2. A Camada de Abstração
Para evitar o acoplamento entre o protocolo e a infraestrutura física (Termux, Linux, Docker, etc.), o sistema utiliza três abstrações fundamentais:
### **1. AST (Abstract Syntax Tree)**
 * **Responsabilidade:** Representa a **sintaxe** do comando.
 * Cada plugin define seu próprio modelo de dados de AST para validar e tipar os parâmetros recebidos.
### **2. IR (Intermediate Representation / Intent)**
 * **Responsabilidade:** Representa o **significado/intenção semântica**.
 * É a camada utilizada por políticas de segurança, sandbox, auditoria e pelo *Protocol Tutor*.
 * **Intenções Suportadas (IntentKind):**
   * READ_RESOURCE: Intenção de carregar/ler conteúdo.
   * MUTATE_RESOURCE: Intenção de modificar o ambiente local.
   * QUERY_STATE: Consulta de estados ou diagnósticos.
   * INSPECT_PROTOCOL: Acesso à ajuda ou metadados do protocolo.
### **3. ISA (Instruction Set Architecture)**
 * **Responsabilidade:** Define o conjunto **finito e imutável de 10 primitivas** executáveis pelo Runtime.
 * **Primitivas Disponíveis (PrimitiveISA):**
   * READ, WRITE, SEARCH, LIST, PATCH, RUN, QUERY, INDEX, SNAPSHOT, HELP.
## 📁 3. Anatomia de um Plugin Autocontido
Todos os comandos de protocolo vivem sob o diretório ~/.termiris/lib/protocol/plugins/. Cada plugin é um pacote Python autocontido:
```path
~/.termiris/lib/protocol/plugins/
└── retrieve/
    ├── __init__.py       # Implementação do plugin (Contrato ProtocolPlugin)
    ├── manifest.json     # Metadados e versão (opcional)
    ├── help.md           # Documentação para a IA/Humanos (opcional)
    └── tests.py          # Testes unitários do plugin (opcional)

```
### O Contrato Obrigatório (ProtocolPlugin)
Todo plugin deve herdar da classe base ProtocolPlugin e implementar seus métodos principais:
```python
from typing import List
from protocol.base import ProtocolPlugin
from protocol.ir import Intent
from protocol.isa import Operation

class ExemploPlugin(ProtocolPlugin):
    @property
    def command(self) -> str:
        """Define a palavra-chave acionadora do comando (ex: RETRIEVE)"""
        return "EXEMPLO"

    def parse_ast(self, tokens: List[str]):
        """Estágio 1: Tokens -> AST (Validação de Sintaxe)"""
        pass

    def lower_to_intent(self, ast_node) -> Intent:
        """Estágio 2: AST -> IR (Geração de Intenção Semântica)"""
        pass

    def lower_to_operations(self, intent: Intent) -> List[Operation]:
        """Estágio 3: IR -> ISA Operations (Geração de Instruções Primitivas)"""
        pass

```
## 🛠️ 4. Guia Prático: Criando um Novo Plugin
Para adicionar uma nova funcionalidade, basta criar um novo diretório na pasta plugins/:
 1. **Crie a pasta do plugin:**
   ```bash
   mkdir -p ~/.termiris/lib/protocol/plugins/search
   
   ```
 2. **Implemente o __init__.py:**
   ```python
   from dataclasses import dataclass
   from typing import List
   from protocol.base import ProtocolPlugin
   from protocol.ir import Intent, IntentKind
   from protocol.isa import Operation, PrimitiveISA
   
   @dataclass(frozen=True)
   class SearchAST:
       query: str
   
   class SearchPlugin(ProtocolPlugin):
       @property
       def command(self) -> str:
           return "SEARCH"
   
       def parse_ast(self, tokens: List[str]) -> SearchAST:
           query_str = " ".join(tokens)
           if not query_str:
               raise ValueError("SEARCH requer um termo de busca.")
           return SearchAST(query=query_str)
   
       def lower_to_intent(self, ast_node: SearchAST) -> Intent:
           return Intent(
               kind=IntentKind.QUERY_STATE,
               target=ast_node.query,
               metadata={"search_type": "text_grep"}
           )
   
       def lower_to_operations(self, intent: Intent) -> List[Operation]:
           return [
               Operation(
                   instruction=PrimitiveISA.SEARCH,
                   payload={"query": intent.target}
               )
           ]
   
   ```
 3. **Invocação:**
   O CommandRouter identificará o novo plugin via *Auto-Discovery* automaticamente na próxima execução.
## 🔒 5. Benefícios Arquiteturais
 * **Zero-Touch Core:** O kernel.py, o CommandRouter e o protocol-handler nunca precisam ser alterados para adicionar, modificar ou deletar comandos.
 * **Testabilidade Isolada:** É possível testar a sintaxe e a geração de instruções de cada plugin sem carregar PTYs, sockets Unix ou acessar o sistema de arquivos.
 * **Segurança por Sandbox:** Como todo comando produz uma Intent intermediária antes de gerar operações físicas, a Sandbox do Termiris pode interceptar e bloquear intenções maliciosas ou não autorizadas de forma centralizada.

