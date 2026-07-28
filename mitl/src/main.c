
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "event_loop.h"
#include "socket_server.h"
#include "pty_proxy.h"

static void resolve_socket_path(char *path, size_t size) {
    const char *xdg = getenv("XDG_RUNTIME_DIR");
    
    if (xdg && xdg[0] != '\0') {
        // Ex: /run/user/1000/termiris/parser.sock
        snprintf(path, size, "%s/termiris", xdg);
        mkdir(path, 0700);
        snprintf(path, size, "%s/termiris/parser.sock", xdg);
    } else {
        // Fallback: ~/.termiris/runtime/parser.sock
        const char *home = getenv("HOME");
        if (!home) {
            fprintf(stderr, "[MITL FATAL] Nem XDG_RUNTIME_DIR nem HOME estao definidos.\n");
            exit(1);
        }
        snprintf(path, size, "%s/.termiris", home);
        mkdir(path, 0700);
        snprintf(path, size, "%s/.termiris/runtime", home);
        mkdir(path, 0700);
        snprintf(path, size, "%s/.termiris/runtime/parser.sock", home);
    }
}

int main(int argc, char **argv) {
    (void)argc;
    event_loop_t loop;
    event_loop_init(&loop);

    char sock_path[256];
    resolve_socket_path(sock_path, sizeof(sock_path));

    socket_server_t sock_server;
    if (socket_server_init(&sock_server, &loop, sock_path) < 0) {
        perror("socket_server_init");
        return 1;
    }

    mitl_sink_t sink = {
        .on_output = on_sink_output,
        .on_resize = NULL,
        .on_exit = NULL,
        .user_data = &sock_server
    };

    char *default_argv[] = { "/bin/bash", NULL };
    char **child_argv = (argv[1] != NULL) ? &argv[1] : default_argv;

    pty_proxy_t proxy;
    if (pty_proxy_init(&proxy, &loop, child_argv, sink) < 0) {
        perror("pty_proxy_init");
        unlink(sock_path);
        return 1;
    }

    printf("[MITL] Engine inicializada. Socket em: %s\n", sock_path);

    event_loop_run(&loop);

    unlink(sock_path);
    return 0;
}
