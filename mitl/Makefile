
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -Iinclude -D_GNU_SOURCE
LDFLAGS = -lutil

SRCS = src/main.c src/event_loop.c src/ring_buffer.c src/socket_server.c src/pty_proxy.c
OBJS = $(SRCS:.c=.o)
TARGET = mitl

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
