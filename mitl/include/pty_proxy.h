
#ifndef PTY_PROXY_H
#define PTY_PROXY_H

#include <termios.h>
#include <sys/types.h>
#include "event_loop.h"
#include "mitl_sink.h"

typedef struct {
    int master_fd;
    pid_t child_pid;
    event_loop_t *loop;
    mitl_sink_t sink;
    struct termios orig_termios;
} pty_proxy_t;

int pty_proxy_init(pty_proxy_t *proxy, event_loop_t *loop, char **child_argv, mitl_sink_t sink);

#endif
