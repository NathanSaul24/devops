#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "tictactoe.h"


void print_board_string() //puts current board as string
{
	int i, j;
	for (i = 0; i < 3; i++) {
		for (j = 0; j < 3; j++) {
			if (b[i][j] == -1) {
				putchar('X');
			} else if (b[i][j] == 1) {
				putchar('O');
			} else {
				putchar('_');
			}
		}
	}
}

int main(int argc, char *argv[]) // handles command-line input and game logic
{
	if (argc != 3) {
		printf("_________|BAD_MOVE\n");
		return 1;
	}

	int i, j, pos = 0;
	for (i = 0; i < 3; i++) {
		for (j = 0; j < 3; j++) {
			char letter = argv[1][pos];
			if (letter == 'X') {
				b[i][j] = -1;
			} else if (letter == 'O') {
				b[i][j] = 1;
			} else {
				b[i][j] = 0;
			}
			pos++;
		}
	}

    // Check if the board is valid
	int move = atoi(argv[2]) - 1;
	if (move < 0 || move > 8) {
		print_board_string();
		printf("|BAD_MOVE\n");
		return 0;
	}

	int hi = move / 3;
	int hj = move % 3;

	if (!is_spot_free(hi, hj)) {
		print_board_string();
		printf("|BAD_MOVE\n");
		return 0;
	}

	b[hi][hj] = 1; 

    // Check for winner or draw after human move
	int winner = check_winner();
	if (winner == 1) {
		print_board_string();
		printf("|O_WINS\n");
		return 0;
	}
	if (board_is_full()) {
		print_board_string();
		printf("|DRAW\n");
		return 0;
	}

// Computer's turn
	test_move(-1, 0);
	b[best_i][best_j] = -1;

	winner = check_winner();
	if (winner == -1) {
		print_board_string();
		printf("|X_WINS\n");
		return 0;
	}
	if (board_is_full()) {
		print_board_string();
		printf("|DRAW\n");
		return 0;
	}

	print_board_string();
	printf("|CONTINUE\n");
	return 0;
}