from copy import deepcopy
import random
PURPLE = (178, 102, 255)

def evaluate_position(board, color):
    # Simple evaluation based on piece count and position
    purple_score = grey_score = 0
    for x in range(8):
        for y in range(8):
            piece = board.getSquare(x, y).squarePiece
            if piece:
                base_score = 10
                if piece.color == PURPLE:
                    purple_score += base_score + (y * 0.5)
                else:
                    grey_score += base_score + ((7-y) * 0.5)
    return purple_score - grey_score if color == PURPLE else grey_score - purple_score

def group1(self, board):
    if self.game.turn != self.color:
        return None, None

    def minimax(board, depth, alpha, beta, maximizing_player, moves_list):
        if depth == 0 or self.endGameCheck(board):
            return evaluate_position(board, self.color), None, None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            moves = list(self.generatemove_at_a_time(board))
            random.shuffle(moves)  # Add randomization to move selection
            
            for row, col, possible_moves in moves:
                for final_pos in possible_moves:
                    move_key = (row, col, final_pos)
                    if move_key in moves_list[-4:]:  # Avoid recent moves
                        continue
                        
                    new_board = deepcopy(board)
                    new_board.move_piece(row, col, final_pos[0], final_pos[1])
                    eval_score, _, _ = minimax(new_board, depth-1, alpha, beta, False, moves_list + [move_key])
                    
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = (row, col), final_pos
                        
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
                        
            return max_eval, best_move[0] if best_move else None, best_move[1] if best_move else None
        else:
            min_eval = float('inf')
            best_move = None
            moves = list(self.generatemove_at_a_time(board))
            random.shuffle(moves)
            
            for row, col, possible_moves in moves:
                for final_pos in possible_moves:
                    move_key = (row, col, final_pos)
                    if move_key in moves_list[-4:]:
                        continue
                        
                    new_board = deepcopy(board)
                    new_board.move_piece(row, col, final_pos[0], final_pos[1])
                    eval_score, _, _ = minimax(new_board, depth-1, alpha, beta, True, moves_list + [move_key])
                    
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = (row, col), final_pos
                        
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
                        
            return min_eval, best_move[0] if best_move else None, best_move[1] if best_move else None

    # Initialize move history if not exists
    if not hasattr(self, 'recent_moves'):
        self.recent_moves = []
        
    # Run minimax with depth 4
    _, current_pos, final_pos = minimax(board, 4, float('-inf'), float('inf'), True, self.recent_moves)
    
    if current_pos and final_pos:
        # Add move to history
        self.recent_moves.append((current_pos[0], current_pos[1], final_pos))
        self.recent_moves = self.recent_moves[-8:]  # Keep last 8 moves
        
        # Validate and return move
        if final_pos in board.get_valid_legal_moves(current_pos[0], current_pos[1], self.game.continue_playing):
            return current_pos, final_pos
            
    return None, None