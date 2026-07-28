
#ifndef RING_BUFFER_H
#define RING_BUFFER_H

#include <stddef.h>
#include <stdint.h>

#define RING_BUFFER_SIZE (64 * 1024) // 64 KB

typedef struct {
    unsigned char data[RING_BUFFER_SIZE];
    uint64_t write_pos; // Posição absoluta de escrita
} ring_buffer_t;

void ring_buffer_init(ring_buffer_t *rb);
void ring_buffer_write(ring_buffer_t *rb, const unsigned char *src, size_t len);
size_t ring_buffer_read_from(const ring_buffer_t *rb, uint64_t *read_pos, unsigned char *dest, size_t max_len, int *bytes_dropped);

#endif
