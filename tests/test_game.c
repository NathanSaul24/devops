#include <stdio.h>
#include <assert.h>
#include "tictactoe.h"

/* Test 1: cant play a taken spot */ 
void test_invalid_move_is_rejected()
{
	reset_board();
	b[1][1] = 1; 

	assert(is_spot_free(1, 1) == 0);
	assert(is_spot_free(0, 0) == 1);

	printf("test_invalid_move_is_rejected passed\n");
}

/* Test 2: check that we spot when the human wins */
void test_detects_human_winner()
{
	reset_board();
	b[0][0] = 1;
	b[0][1] = 1;
	b[0][2] = 1;

	assert(check_winner() == 1);

	printf("test_detects_human_winner passed\n");
}

/* Test 3: check that we spot when the computer wins */
void test_detects_computer_winner()
{
	reset_board();
	b[0][1] = -1;
	b[1][1] = -1;
	b[2][1] = -1;

	assert(check_winner() == -1);

	printf("test_detects_computer_winner passed\n");
}

/* Test 4: computer takes obvious winning move */
void test_computer_takes_winning_move()
{
	reset_board();
	b[0][0] = -1;
	b[0][1] = -1;
	b[1][0] = 1;
	b[1][1] = 1;

	test_move(-1, 0);

	assert(best_i == 0);
	assert(best_j == 2);

	printf("test_computer_takes_winning_move passed\n");
}

int main()
{
	test_invalid_move_is_rejected();
	test_detects_human_winner();
	test_detects_computer_winner();
	test_computer_takes_winning_move();

	printf("\nAll tests passed!\n");
	return 0;
}