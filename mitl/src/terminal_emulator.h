#ifndef TERMINAL_EMULATOR_H
#define TERMINAL_EMULATOR_H

#include <stddef.h>

#define TERM_ROWS 64
#define TERM_COLS 512

typedef struct {
    char screen[TERM_ROWS][TERM_COLS];
    size_t row;
    size_t col;

    enum {
        TE_NORMAL,
        TE_ESC,
        TE_CSI
    } state;

    char csi[64];
    size_t csi_len;
    int dirty;
} terminal_emulator_t;

void terminal_emulator_init(terminal_emulator_t *te);

void terminal_emulator_feed(
    terminal_emulator_t *te,
    const unsigned char *data,
    size_t len
);

const char *terminal_emulator_visible_text(
    terminal_emulator_t *te
);

#endif
