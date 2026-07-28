
#define _GNU_SOURCE
#include "pty_proxy.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <sys/ioctl.h>

#if defined(__APPLE__) || defined(__FreeBSD__)
#include <util.h>
#else
#include <pty.h>
#endif

static pty_proxy_t *g_proxy_ref = NULL;

static void set_raw_mode(struct termios *orig) {
    tcgetattr(STDIN_FILENO, orig);
    struct termios raw = *orig;
    cfmakeraw(&raw);
    tcsetattr(STDIN_FILENO, TCSANOW, &raw);
}

static void restore_mode(void) {
    if (g_proxy_ref) {
        tcsetattr(STDIN_FILENO, TCSANOW, &g_proxy_ref->orig_termios);
    }
}

static void on_pty_master_read(int fd, void *arg) {
    pty_proxy_t *proxy = (pty_proxy_t *)arg;
    unsigned char buf[1024];
    ssize_t n = read(fd, buf, sizeof(buf));

    if (n > 0) {
        ssize_t unused = write(STDOUT_FILENO, buf, n);
        (void)unused;

        if (proxy->sink.on_output) {
            proxy->sink.on_output(buf, (size_t)n, proxy->sink.user_data);
        }
    } else if (n <= 0) {
        proxy->loop->running = 0;
    }
}

static void on_stdin_read(int fd, void *arg) {
    pty_proxy_t *proxy = (pty_proxy_t *)arg;
    unsigned char buf[1024];
    ssize_t n = read(fd, buf, sizeof(buf));

    if (n > 0) {
        ssize_t unused = write(proxy->master_fd, buf, n);
        (void)unused;
    }
}

static void handle_sigwinch(int sig) {
    (void)sig;
    if (!g_proxy_ref) return;
    struct winsize ws;
    if (ioctl(STDIN_FILENO, TIOCGWINSZ, &ws) == 0) {
        ioctl(g_proxy_ref->master_fd, TIOCSWINSZ, &ws);
        if (g_proxy_ref->sink.on_resize) {
            g_proxy_ref->sink.on_resize(ws.ws_row, ws.ws_col, g_proxy_ref->sink.user_data);
        }
    }
}

int pty_proxy_init(pty_proxy_t *proxy, event_loop_t *loop, char **child_argv, mitl_sink_t sink) {
    proxy->loop = loop;
    proxy->sink = sink;
    g_proxy_ref = proxy;

    struct winsize ws;
    ioctl(STDIN_FILENO, TIOCGWINSZ, &ws);

    proxy->child_pid = forkpty(&proxy->master_fd, NULL, NULL, &ws);
    if (proxy->child_pid < 0) return -1;

    if (proxy->child_pid == 0) {
        execvp(child_argv[0], child_argv);
        perror("execvp");
        exit(1);
    }

    fcntl(proxy->master_fd, F_SETFL, O_NONBLOCK);
    fcntl(STDIN_FILENO, F_SETFL, O_NONBLOCK);

    event_loop_add(loop, proxy->master_fd, POLLIN, on_pty_master_read, proxy);
    event_loop_add(loop, STDIN_FILENO, POLLIN, on_stdin_read, proxy);

    set_raw_mode(&proxy->orig_termios);
    atexit(restore_mode);

    signal(SIGWINCH, handle_sigwinch);

    return 0;
}
