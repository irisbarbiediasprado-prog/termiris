colar(){ local cmd; cmd="$(termux-clipboard-get)"; printf "[1;36m>>> %s[0m
" "$cmd"; builtin eval "$cmd"; }
leader(){ tmux send-prefix; }
new_window(){ tmux new-window; }
split_h(){ tmux split-window -h; }
split_v(){ tmux split-window -v; }
next_window(){ tmux next-window; }
prev_window(){ tmux previous-window; }
