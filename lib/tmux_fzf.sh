tmux_fzf() {
    if [ -z "$TMUX" ]; then
        fzf "$@"
        return
    fi

    if tmux display-popup -E true >/dev/null 2>&1; then
        tmux popup -w 100% -h 100% -E "fzf $*"
    else
        tmux split-window -vf "fzf $*; printf '\n[Enter]'; read _"
    fi
}
