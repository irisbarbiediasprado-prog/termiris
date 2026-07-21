#!/data/data/com.termux/files/usr/bin/bash

tmux_fzf() {
  local title="${1:-Selecionar}"
  shift || true

  fzf \
    --prompt="$title > " \
    --height=80% \
    --border \
    --reverse
}
