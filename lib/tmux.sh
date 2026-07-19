new_window(){ tmux new-window; }
kill_window(){ tmux kill-window; }
split_h(){ tmux split-window -h; }
split_v(){ tmux split-window -v; }
next_window(){ tmux next-window; }
prev_window(){ tmux previous-window; }
last_window(){ tmux last-window; }
rename_window(){ tmux command-prompt -p "Nome:" "rename-window %%"; }
tmux_version(){ tmux -V; }
