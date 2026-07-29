#include "protocol_extractor.h"

#include <stdint.h>
#include <string.h>

static uint64_t fnv1a(const char *s, size_t n) {
    uint64_t h = 1469598103934665603ULL;

    for (size_t i = 0; i < n; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ULL;
    }

    return h;
}

void protocol_extractor_init(protocol_extractor_t *pe) {
    pe->last_hash = 0;
}

void protocol_extractor_scan(
    protocol_extractor_t *pe,
    const char *screen,
    protocol_tag_callback cb,
    void *user_data
) {
    const char *p = screen;

    while ((p = strstr(p, "<<")) != NULL) {

        const char *end = strstr(p + 2, ">>");
        if (!end)
            break;

        size_t len = (size_t)(end - p + 2);

        uint64_t hash = fnv1a(p, len);

        if (hash != pe->last_hash) {
            pe->last_hash = hash;
            cb(
                (const unsigned char *)p,
                len,
                user_data
            );
        }

        p = end + 2;
    }
}
