#ifndef TICTACTOE_H
#define TICTACTOE_H

extern int b[3][3]; /* board. 0: blank; -1: computer; 1: human */
extern int best_i, best_j;

void reset_board();
int is_spot_free(int i, int j);
int check_winner();
void showboard();
int test_move(int val, int depth);
const char* game(int user);

#endif