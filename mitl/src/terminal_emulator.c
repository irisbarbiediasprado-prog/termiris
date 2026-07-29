#include "terminal_emulator.h"

#include <string.h>
#include <unistd.h>

static void newline(terminal_emulator_t *te) {
    if (te->row + 1 < TERM_ROWS)
        te->row++;
    te->col = 0;
}

void terminal_emulator_init(terminal_emulator_t *te) {
    memset(te, 0, sizeof(*te));

    for (size_t r = 0; r < TERM_ROWS; r++)
        memset(te->screen[r], ' ', TERM_COLS);

    te->state = TE_NORMAL;
}

void terminal_emulator_feed(
    terminal_emulator_t *te,
    const unsigned char *data,
    size_t len
) {
    (void)write(STDOUT_FILENO, data, len);

    for (size_t i = 0; i < len; i++) {
        unsigned char c = data[i];

        switch (te->state) {

        case TE_NORMAL:

            if (c == 0x1b) {
                te->state = TE_ESC;
                continue;
            }

            if (c == '\r') {
                te->col = 0;
                continue;
            }

            if (c == '\n') {
                newline(te);
                continue;
            }

            if (c == '\b') {
                if (te->col)
                    te->col--;
                continue;
            }

            if (c >= 32 && c < 127) {
                if (te->row < TERM_ROWS && te->col < TERM_COLS)
                    te->screen[te->row][te->col++] = (char)c;
            }

            break;

        case TE_ESC:

            if (c == '[') {
                te->state = TE_CSI;
                te->csi_len = 0;
            } else {
                te->state = TE_NORMAL;
            }

            break;

        case TE_CSI:

            if ((c >= '@' && c <= '~') || te->csi_len >= sizeof(te->csi)-1) {

                te->csi[te->csi_len] = '\0';

                switch (c) {

                case 'J':
                    memset(te->screen, ' ', sizeof(te->screen));
                    te->row = 0;
                    te->col = 0;
                    break;

                case 'K':
                    memset(
                        &te->screen[te->row][te->col],
                        ' ',
                        TERM_COLS - te->col
                    );
                    break;

                default:
                    break;
                }

                te->state = TE_NORMAL;

            } else {

                te->csi[te->csi_len++] = (char)c;

            }

            break;
        }
    }
}

const char *terminal_emulator_visible_text(
    terminal_emulator_t *te
) {
    static char buffer[TERM_ROWS * (TERM_COLS + 1)];

    char *p = buffer;

    for (size_t r = 0; r < TERM_ROWS; r++) {
        memcpy(p, te->screen[r], TERM_COLS);
        p += TERM_COLS;
        *p++ = '\n';
    }

    *p = '\0';

    return buffer;
}
