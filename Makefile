CC = gcc
CFLAGS = -Wall -std=c99

game.exe: game/main.c
	$(CC) $(CFLAGS) -o game.exe game/main.c

clean:
	rm -f game.exe