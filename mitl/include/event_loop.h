
#ifndef EVENT_LOOP_H
#define EVENT_LOOP_H

#include <poll.h>

#define MAX_POLL_FDS 64

typedef struct event_loop {
    struct pollfd fds[MAX_POLL_FDS];
    void (*handlers[MAX_POLL_FDS])(int fd, void *arg);
    void *args[MAX_POLL_FDS];
    int count;
    int running;
} event_loop_t;

void event_loop_init(event_loop_t *loop);
int event_loop_add(event_loop_t *loop, int fd, short events, void (*handler)(int, void*), void *arg);
void event_loop_remove(event_loop_t *loop, int fd);
void event_loop_run(event_loop_t *loop);

#endif
