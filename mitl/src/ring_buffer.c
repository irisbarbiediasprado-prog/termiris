
#include "ring_buffer.h"
#include <string.h>

void ring_buffer_init(ring_buffer_t *rb) {
    rb->write_pos = 0;
    memset(rb->data, 0, RING_BUFFER_SIZE);
}

void ring_buffer_write(ring_buffer_t *rb, const unsigned char *src, size_t len) {
    for (size_t i = 0; i < len; i++) {
        rb->data[rb->write_pos % RING_BUFFER_SIZE] = src[i];
        rb->write_pos++;
    }
}

size_t ring_buffer_read_from(const ring_buffer_t *rb, uint64_t *read_pos, unsigned char *dest, size_t max_len, int *bytes_dropped) {
    if (bytes_dropped) *bytes_dropped = 0;

    if (rb->write_pos > *read_pos + RING_BUFFER_SIZE) {
        uint64_t dropped = rb->write_pos - RING_BUFFER_SIZE - *read_pos;
        if (bytes_dropped) *bytes_dropped = (int)dropped;
        *read_pos = rb->write_pos - RING_BUFFER_SIZE;
    }

    size_t available = (size_t)(rb->write_pos - *read_pos);
    size_t to_read = (available < max_len) ? available : max_len;

    for (size_t i = 0; i < to_read; i++) {
        dest[i] = rb->data[(*read_pos) % RING_BUFFER_SIZE];
        (*read_pos)++;
    }

    return to_read;
}
