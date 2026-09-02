CC = gcc
CFLAGS = -Wall -std=c99 # basic params

all: game.exe engine_move

game.exe: game/main.c game/tictactoe.c game/tictactoe.h
	$(CC) $(CFLAGS) -o game.exe game/main.c game/tictactoe.c

engine_move: game/engine_cli.c game/tictactoe.c game/tictactoe.h
	$(CC) $(CFLAGS) -o engine_move game/engine_cli.c game/tictactoe.c

tests.exe: tests/test_game.c game/tictactoe.c game/tictactoe.h
	$(CC) $(CFLAGS) -I game -o tests.exe tests/test_game.c game/tictactoe.c

test: tests.exe
	./tests.exe

clean:
	rm -f game.exe tests.exe engine_move