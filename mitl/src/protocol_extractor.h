#ifndef PROTOCOL_EXTRACTOR_H
#define PROTOCOL_EXTRACTOR_H

#include <stddef.h>
#include <stdint.h>

typedef struct {
    uint64_t last_hash;
} protocol_extractor_t;

typedef void (*protocol_tag_callback)(
    const unsigned char *tag,
    size_t len,
    void *user_data
);

void protocol_extractor_init(
    protocol_extractor_t *pe
);

void protocol_extractor_scan(
    protocol_extractor_t *pe,
    const char *screen,
    protocol_tag_callback cb,
    void *user_data
);

#endif
