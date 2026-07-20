# Termiris — Terminal + Iris

Ambiente de desenvolvimento persistente e automatizado para Termux, construído sobre tmux, fzf e uma filosofia de **um comando, uma ação, um resultado**.

---

## Filosofia

Termiris nasceu da ideia de que um terminal em um smartphone deve ser tão produtivo quanto em um desktop — mas com menos atrito.

Cada ferramenta tem uma responsabilidade única:
- **Termux** → interface com o Android (clipboard, compartilhamento, notificações)
- **tmux** → sessões persistentes, janelas e painéis
- **fzf** → navegação e seleção fuzzy
- **Bash** → orquestração e automação

Toda interação é pensada para ser executada com um único toque ou comando.
O crescimento do projeto ocorre através da evolução da barra de **extra-keys** do Termux, nunca exigindo que o usuário memorize comandos complexos.

---

## Tecnologias principais

| Ferramenta | Função |
|------------|--------|
| `tmux` | Multiplexador de terminal |
| `fzf` | Busca fuzzy interativa |
| `fd` | Finder de arquivos rápido |
| `bat` | Preview de arquivos com syntax highlight |
| `zoxide` | Navegação inteligente por diretórios |
| `git` | Versionamento |
| `Neovim` | Editor (opcional) |
| `Termux:API` | Clipboard, notificações e compartilhamento |

---

## Estrutura do projeto

```
~/.termiris/
├── bin/               # Comandos executáveis (ff, buscar, nav, colar, copiar, check)
├── config/            # Arquivos de configuração (bashrc, tmux.conf, termux.properties)
├── lib/               # Funções compartilhadas (core.sh)
├── init.sh            # Carregamento do ambiente
└── README.md          # Este arquivo
```

Symlinks apontam para dentro do projeto:
- `~/.bashrc` → `~/.termiris/config/bashrc`
- `~/.tmux.conf` → `~/.termiris/config/tmux.conf`
- `~/.termux/termux.properties` → `~/.termiris/config/termux.properties`

---

## Instalação

```bash
git clone git@github.com:irisbarbiediasprado-prog/termiris.git ~/.termiris
cd ~/.termiris && ./install.sh   # (em breve)
```

Ou, se você já tem o projeto, basta recarregar o shell:

```bash
source ~/.bashrc
```

---

## Atalhos da barra extra-keys

| Ícone | Tecla | Ação |
|-------|-------|------|
| ➕ | `ALT+c` | Nova janela tmux |
| ▶ | `ALT+n` | Próxima janela |
| ✕ | `kill_window\n` | Fechar janela atual |
| 📥 | `ALT+v` | Colar conteúdo do clipboard (via tmux buffer) |
| 📋 | `ALT+y` | Copiar conteúdo do painel atual |
| 🔍 | `ALT+b` | Buscar arquivos com fzf e abrir no Android |

---

## Comandos disponíveis

| Comando | Função |
|---------|--------|
| `ff` | Abrir seletor de arquivos (fzf + preview) e abrir no Android |
| `buscar` | Buscar arquivos com preview (similar ao ff, mas sem abrir) |
| `nav` | Navegar por diretórios recentes (zoxide + fzf) e abrir nova janela tmux |
| `colar` | Colar conteúdo do clipboard no tmux |
| `copiar` | Copiar conteúdo do painel tmux para o clipboard |
| `check` | Verificar sanidade do ambiente (dependências, symlinks, permissões) |

---

## Como evoluir

O projeto é modular. Para adicionar um novo comando:
1. Crie um script em `bin/` com shebang `#!/data/data/com.termux/files/usr/bin/bash`
2. Se precisar de funções compartilhadas, adicione em `lib/core.sh`
3. Para vincular a uma tecla, edite `config/tmux.conf` e `config/termux.properties`

Sempre priorize:
- **Um comando, uma ação, um resultado**
- **Automação acima de memorização**
- **Menos arquivos, menos dependências, menos decisões**

---

## Licença

MIT — use, modifique, compartilhe.

Feito com ❤️ para quem quer programar no celular sem dor de cabeça.
