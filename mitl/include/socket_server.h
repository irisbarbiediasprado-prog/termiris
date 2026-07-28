
#ifndef SOCKET_SERVER_H
#define SOCKET_SERVER_H

#include "event_loop.h"
#include "ring_buffer.h"

typedef struct client_node {
    int fd;
    uint64_t read_pos;
    struct client_node *next;
} client_node_t;

typedef struct {
    int server_fd;
    ring_buffer_t rb;
    client_node_t *clients;
    event_loop_t *loop;
} socket_server_t;

int socket_server_init(socket_server_t *server, event_loop_t *loop, const char *path);
void on_sink_output(const unsigned char *data, size_t len, void *user_data);

#endif
