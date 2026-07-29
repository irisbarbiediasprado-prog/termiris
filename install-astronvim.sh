#!/usr/bin/env bash
set -e

echo "🚀 Iniciando a instalação do AstroNvim (Spacemacs Style + Nyan Cat Vibe)..."

# 1. Verificar dependências essenciais
command -v nvim >/dev/null 2>&1 || { echo "❌ Erro: Neovim não encontrado. Instale o Neovim >= 0.9.5."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Erro: Git não encontrado."; exit 1; }
command -v make >/dev/null 2>&1 || { echo "❌ Erro: Make não encontrado."; exit 1; }
command -v rg >/dev/null 2>&1 || { echo "⚠️ Aviso: ripgrep (rg) não encontrado. É altamente recomendado para buscas no projeto."; }

NVIM_DIR="$HOME/.config/nvim"
NVIM_BACKUP="$HOME/.config/nvim.bak.$(date +%Y%m%d_%H%M%S)"

# 2. Backup de configurações existentes
if [ -d "$NVIM_DIR" ]; then
    echo "📦 Fazendo backup da configuração antiga para $NVIM_BACKUP..."
    mv "$NVIM_DIR" "$NVIM_BACKUP"
fi

# 3. Clonar o template base do AstroNvim
echo "📥 Clonando o template oficial do AstroNvim..."
git clone --depth 1 https://github.com/AstroNvim/template "$NVIM_DIR"

# Remover o .git do template para você poder inicializar o SEU repositório versionado depois
rm -rf "$NVIM_DIR/.git"

echo "🎨 Criando as configurações personalizadas (Tema Catppuccin / Nyan Cat & Spacemacs Keymaps)..."

# Criar diretórios necessários caso não existam
mkdir -p "$NVIM_DIR/lua/plugins"

# 4. Criar o arquivo de tema (Catppuccin Mocha - pegada cósmica de arco-íris)
cat << 'EOF' > "$NVIM_DIR/lua/plugins/nyan-theme.lua"
return {
  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    opts = {
      flavour = "mocha", -- "mocha" dá um contraste vibrante com cores vivas e espaciais
      transparent_background = false,
      term_colors = true,
      integrations = {
        which_key = true,
        notify = true,
        mini = true,
      },
    },
  },
  {
    "AstroNvim/astronvim",
    opts = {
      colorscheme = "catppuccin-mocha",
    },
  },
}
EOF

# 5. Criar o plugin do Nyan Cat real
cat << 'EOF' > "$NVIM_DIR/lua/plugins/nyancat.lua"
return {
  "jserv/nyancat.vim",
  cmd = "Nyan",
  keys = {
    { "<leader>fn", "<cmd>Nyan<cr>", desc = "Nyan Cat Mode!" },
  },
  config = function()
    vim.g.nyancat_scale = 0.6
    vim.g.nyancat_rainbow_border = 1
    vim.g.nyancat_message = "Nyan nyan nyan!"
  end,
}
EOF

# 6. Criar o arquivo de mapeamentos estilo Spacemacs
cat << 'EOF' > "$NVIM_DIR/lua/plugins/user.lua"
return {
  {
    "AstroNvim/astrocore",
    opts = {
      options = {
        opt = {
          relativenumber = true, -- Essencial para navegação modal estilo Spacemacs/Evil
          mouse = "a",
        },
      },
      mappings = {
        n = {
          -- Spacemacs shortcuts básicos
          ["<leader>fs"] = { ":w<CR>", desc = "Salvar arquivo" },
          ["<leader>qq"] = { ":qa<CR>", desc = "Sair do Neovim" },
        },
      },
    },
  },
}
EOF
# Cria o diretório de plugins caso ele não exista
mkdir -p ~/.config/nvim/lua/plugins

# Grava as configurações diretamente no arquivo user.lua
cat << 'EOF' > ~/.config/nvim/lua/plugins/user.lua
return {
  {
    "AstroNvim/astrocore",
    opts = {
      options = {
        opt = {
          number = false,
          relativenumber = false,
          signcolumn = "no",
          showcmd = true,
          cursorline = false,
          showtabline = 0,
          laststatus = 3,
          cmdheight = 1,
        },
      },
    },
  },
  {
    "akinsho/bufferline.nvim",
    enabled = false,
  },
  {
    "jserv/nyancat.vim",
    cmd = "Nyan",
  },
}
EOF

echo "✨ Tudo pronto! O ambiente foi configurado com sucesso em $NVIM_DIR."
echo "👉 Agora execute 'nvim' no seu terminal para baixar os plugins automaticamente e aproveitar o seu AstroNvim com tema espacial e Nyan Cat!"
