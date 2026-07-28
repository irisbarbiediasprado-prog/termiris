
#include "event_loop.h"
#include <stdio.h>
#include <errno.h>

void event_loop_init(event_loop_t *loop) {
    loop->count = 0;
    loop->running = 1;
}

int event_loop_add(event_loop_t *loop, int fd, short events, void (*handler)(int, void*), void *arg) {
    if (loop->count >= MAX_POLL_FDS) return -1;
    loop->fds[loop->count].fd = fd;
    loop->fds[loop->count].events = events;
    loop->fds[loop->count].revents = 0;
    loop->handlers[loop->count] = handler;
    loop->args[loop->count] = arg;
    loop->count++;
    return 0;
}

void event_loop_remove(event_loop_t *loop, int fd) {
    for (int i = 0; i < loop->count; i++) {
        if (loop->fds[i].fd == fd) {
            for (int j = i; j < loop->count - 1; j++) {
                loop->fds[j] = loop->fds[j + 1];
                loop->handlers[j] = loop->handlers[j + 1];
                loop->args[j] = loop->args[j + 1];
            }
            loop->count--;
            break;
        }
    }
}

void event_loop_run(event_loop_t *loop) {
    while (loop->running && loop->count > 0) {
        int ret = poll(loop->fds, loop->count, -1);
        if (ret < 0) {
            if (errno == EINTR) continue;
            perror("poll");
            break;
        }

        int current_count = loop->count;
        for (int i = 0; i < current_count; i++) {
            if (loop->fds[i].revents & (POLLIN | POLLHUP | POLLERR)) {
                if (loop->handlers[i]) {
                    loop->handlers[i](loop->fds[i].fd, loop->args[i]);
                }
            }
        }
    }
}
