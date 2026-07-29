#include "protocol_extractor.h"

#include <string.h>

void protocol_extractor_init(protocol_extractor_t *pe) {
    pe->len = 0;
}

void protocol_extractor_feed(
    protocol_extractor_t *pe,
    const unsigned char *data,
    size_t len,
    protocol_tag_callback cb,
    void *user_data
) {
    for (size_t i = 0; i < len; i++) {
        unsigned char c = data[i];

        /* buffer cheio: reinicia procurando próxima tag */
        if (pe->len >= PROTOCOL_EXTRACTOR_MAX - 1)
            pe->len = 0;

        pe->buffer[pe->len++] = c;

        /* ainda não tem "<<": mantém apenas possível '<' */
        if (pe->len == 1) {
            if (pe->buffer[0] != '<')
                pe->len = 0;
            continue;
        }

        if (pe->len == 2) {
            if (pe->buffer[0] != '<' || pe->buffer[1] != '<') {
                if (pe->buffer[1] == '<') {
                    pe->buffer[0] = '<';
                    pe->len = 1;
                } else {
                    pe->len = 0;
                }
            }
            continue;
        }

        /* fechou ">>" */
        if (pe->buffer[pe->len - 2] == '>' &&
            pe->buffer[pe->len - 1] == '>') {

            if (cb)
                cb(pe->buffer, pe->len, user_data);

            pe->len = 0;
        }
    }
}
