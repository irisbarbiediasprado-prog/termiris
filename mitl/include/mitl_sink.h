
#ifndef MITL_SINK_H
#define MITL_SINK_H

#include <stddef.h>

typedef struct mitl_sink {
    void (*on_output)(const unsigned char *data, size_t len, void *user_data);
    void (*on_resize)(int rows, int cols, void *user_data);
    void (*on_exit)(int exit_code, void *user_data);
    void *user_data;
} mitl_sink_t;

#endif
