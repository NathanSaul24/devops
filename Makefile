CC = gcc
CFLAGS = -Wall -std=c99 # basic params

game.exe: game/main.c game/tictactoe.c game/tictactoe.h # Builds game.exe from main.c
	$(CC) $(CFLAGS) -o game.exe game/main.c game/tictactoe.c

tests.exe: tests/test_game.c game/tictactoe.c game/tictactoe.h
	$(CC) $(CFLAGS) -I game -o tests.exe tests/test_game.c game/tictactoe.c

test: tests.exe
	./tests.exe

clean: # Deletes game.exe and tests.exe
	rm -f game.exe tests.exe