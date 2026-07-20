#!/data/data/com.termux/files/usr/bin/bash
colar_buffer(){ local tmp="$HOME/.cache/tmux-clipboard"; mkdir -p "$(dirname "$tmp")" && termux-clipboard-get > "$tmp" 2>/dev/null && tmux load-buffer "$tmp" 2>/dev/null && tmux paste-buffer 2>/dev/null && tmux send-keys Enter 2>/dev/null; }
copiar(){ tmux capture-pane -pS - 2>/dev/null | termux-clipboard-set 2>/dev/null; }
new_window(){ tmux new-window 2>/dev/null; }
kill_window(){ tmux kill-window 2>/dev/null; }
split_h(){ tmux split-window -h 2>/dev/null; }
split_v(){ tmux split-window -v 2>/dev/null; }
next_window(){ tmux next-window 2>/dev/null; }
prev_window(){ tmux previous-window 2>/dev/null; }
last_window(){ tmux last-window 2>/dev/null; }
rename_window(){ tmux command-prompt -p "Nome:" "rename-window %%" 2>/dev/null; }
tmux_version(){ tmux -V 2>/dev/null; }
select_file(){ local dir="${1:-.}"; (cd "$dir" 2>/dev/null || return 1; fd --type f --hidden --follow --exclude .git --strip-cwd-prefix . 2>/dev/null | fzf --height=100% --layout=reverse --border=none --info=inline --prompt="📄 Arquivos > " --preview='bat --style=numbers --color=always --line-range=:200 {}' --preview-window='down,35%,border-top,wrap'); }
ff(){ local f; f="$(select_file "${1:-.}")" || return; am start -a android.intent.action.VIEW -d "file://$(realpath "$f" 2>/dev/null)" -t "*/*" >/dev/null 2>&1 && printf '✓ %s\n' "$f"; }
