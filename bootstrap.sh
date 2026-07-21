#!/data/data/com.termux/files/usr/bin/bash
set -euxo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "==> Selecionando mirror..."
termux-change-repo

echo "==> Atualizando pacotes..."
yes | pkg update

echo "==> Instalando dependências..."
yes | pkg install \

for c in git ssh tmux termux-reload-settings fd fzf bat rg eza zoxide zip cargo rustc aichat yq; do command -v "$c" >/dev/null || { echo "❌ Dependência ausente: $c"; exit 1; }; done

  git \
  openssh \
  tmux \
  termux-api \
  fzf \
  fd \
  bat \
  ripgrep \
  eza \
  zoxide \
  curl \
  yq \
  zip \
  rust \
  aichat

echo "==> Criando diretórios..."
mkdir -p ~/.termux ~/.config ~/.config/aichat

echo "==> Criando symlinks..."
ln -snf "$ROOT/config/bashrc" ~/.bashrc
ln -snf "$ROOT/config/tmux.conf" ~/.tmux.conf
ln -snf "$ROOT/config/termux.properties" ~/.termux/termux.properties

echo "==> Configurando aichat..."
"$ROOT/bin/configure-aichat"

echo "==> Recarregando Termux..."
termux-reload-settings || true

echo "==> Reiniciando shell..."
exec bash
