# Simple build without CMake: `make` (OpenMP) or `make SERIAL=1` (single-threaded).
CC ?= gcc
CFLAGS = -O3 -Wall -Wextra -std=c11
LDFLAGS = -lm

ifndef SERIAL
    CFLAGS += -fopenmp
    LDFLAGS += -fopenmp
endif

SRC = src/main.c src/engine.c src/forcefield.c src/xyz_io.c
BIN = evm_engine

$(BIN): $(SRC) src/*.h
	$(CC) $(CFLAGS) -o $(BIN) $(SRC) $(LDFLAGS)

clean:
	rm -f $(BIN) $(BIN).exe

.PHONY: clean
