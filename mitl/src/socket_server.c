#include "socket_server.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/un.h>

static void socket_server_broadcast(socket_server_t *server) {
    client_node_t **curr = &server->clients;
    unsigned char buf[1024];

    while (*curr) {
        int bytes_dropped = 0;
        size_t n = ring_buffer_read_from(&server->rb, &(*curr)->read_pos, buf, sizeof(buf), &bytes_dropped);

        if (bytes_dropped > 0) {
            fprintf(stderr, "\n[MITL WARN] Cliente FD %d perdeu %d bytes (consumidor lento). Desconectando.\n", (*curr)->fd, bytes_dropped);
            client_node_t *tmp = *curr;
            close(tmp->fd);
            event_loop_remove(server->loop, tmp->fd);
            *curr = tmp->next;
            free(tmp);
            continue;
        }

        if (n > 0) {
            fprintf(stderr,
                "[SOCKET] %zd bytes: %.*s\n",
                n,
                (int)n,
                buf);
	    ssize_t written = write((*curr)->fd, buf, n);
            if (written <= 0) {
                client_node_t *tmp = *curr;
                close(tmp->fd);
                event_loop_remove(server->loop, tmp->fd);
                *curr = tmp->next;
                free(tmp);
                continue;
            }
        }
        curr = &(*curr)->next;
    }
}

void on_sink_output(const unsigned char *data, size_t len, void *user_data) {
    socket_server_t *server = (socket_server_t *)user_data;
    ring_buffer_write(&server->rb, data, len);
    socket_server_broadcast(server);
}

static void on_client_read(int fd, void *arg) {
    (void)arg;
    unsigned char dummy[64];
    if (read(fd, dummy, sizeof(dummy)) <= 0) {
        // Trado em falha de escrita no broadcast
    }
}

static void on_new_connection(int server_fd, void *arg) {
    socket_server_t *server = (socket_server_t *)arg;
    int client_fd = accept(server_fd, NULL, NULL);
    if (client_fd < 0) return;

    fcntl(client_fd, F_SETFL, O_NONBLOCK);

    client_node_t *node = malloc(sizeof(client_node_t));
    node->fd = client_fd;
    node->read_pos = server->rb.write_pos;
    node->next = server->clients;
    server->clients = node;

    event_loop_add(server->loop, client_fd, POLLIN, on_client_read, server);
    printf("\n[MITL] Novo cliente conectado no Socket Unix (FD: %d)\n", client_fd);
}

int socket_server_init(socket_server_t *server, event_loop_t *loop, const char *path) {
    server->loop = loop;
    server->clients = NULL;
    ring_buffer_init(&server->rb);

    unlink(path);
    server->server_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (server->server_fd < 0) return -1;

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, path, sizeof(addr.sun_path) - 1);

    if (bind(server->server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) return -1;
    if (listen(server->server_fd, 5) < 0) return -1;

    fcntl(server->server_fd, F_SETFL, O_NONBLOCK);
    event_loop_add(loop, server->server_fd, POLLIN, on_new_connection, server);

    return 0;
}
