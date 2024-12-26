# We have used the Minimax algorithm with Alpha-Beta pruning to determine the best move.
from copy import deepcopy
PURPLE = (178, 102, 255)  
def group1(self, board):
    if self.game.turn != self.color:  # Only move if it's this AI's turn
        return None, None

    tr_table = {}
    def minimax(board, depth, alpha, beta, max_player):
        board_hash = hash(str(board.matrix))  
        if board_hash in tr_table and tr_table[board_hash][1] >= depth:
            return tr_table[board_hash][0], None, None

        if depth == 0 or self.endGameCheck(board):
            eval = self._current_eval(board)
            tr_table[board_hash] = (eval, depth)
            return eval, None, None

        if max_player:
            max_eval = float('-inf')
            best_move = None
            for row, col, possible_moves in self.generatemove_at_a_time(board):  
                current_pos = (row, col)  
                possible_moves.sort(key=lambda move: abs(move[0] - 7) if self.color == PURPLE 
                                     else abs(move[0] - 0), reverse=True)  
                for final_pos in possible_moves:
                    # Apply the move
                    new_board = deepcopy(board)
                    new_board.move_piece(row, col, final_pos[0], final_pos[1])
                    eval, _, _ = minimax(new_board, depth-1, alpha, beta, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (current_pos, final_pos)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            tr_table[board_hash] = (max_eval, depth)
            return max_eval, best_move[0], best_move[1] if best_move else (None, None)
        else:
            min_eval = float('inf')
            best_move = None
            for row, col, possible_moves in self.generatemove_at_a_time(board):
                current_pos = (row, col)
                for final_pos in possible_moves:
                    # Apply the move
                    new_board = deepcopy(board)
                    new_board.move_piece(row, col, final_pos[0], final_pos[1])
                    eval, _, _ = minimax(new_board, depth-1, alpha, beta, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (current_pos, final_pos)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            tr_table[board_hash] = (min_eval, depth)
            return min_eval, best_move[0], best_move[1] if best_move else (None, None)
    
    _, current_pos, final_pos = minimax(board, self.depth, float('-inf'), float('inf'), True)

    if current_pos is None or final_pos is None:
        return None, None

    # Validate move
    if final_pos in board.get_valid_legal_moves(current_pos[0], current_pos[1], self.game.continue_playing):
        return current_pos, final_pos
    return None, None