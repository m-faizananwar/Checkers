from copy import deepcopy
PURPLE = (178, 102, 255)

def evaluate_board(board, color):
    purple_score = grey_score = 0
    for x in range(8):
        for y in range(8):
            piece = board.getSquare(x, y).squarePiece
            if piece:
                base_value = 10
                # Give higher value to pieces closer to promotion
                if piece.color == PURPLE:
                    position_value = y * 1.5  # More value for pieces closer to bottom
                    purple_score += base_value + position_value
                else:
                    position_value = (7-y) * 1.5  # More value for pieces closer to top
                    grey_score += base_value + position_value
                
                # Bonus for protected pieces
                if is_protected(board, x, y):
                    if piece.color == PURPLE:
                        purple_score += 3
                    else:
                        grey_score += 3
                        
    return purple_score - grey_score if color == PURPLE else grey_score - purple_score

def is_protected(board, x, y):
    """Check if a piece is protected by friendly pieces"""
    piece = board.getSquare(x, y).squarePiece
    if not piece:
        return False
    
    adjacent_squares = board.getAdjacentSquares(x, y)
    for ax, ay in adjacent_squares:
        if board.within_bounds(ax, ay):
            adj_piece = board.getSquare(ax, ay).squarePiece
            if adj_piece and adj_piece.color == piece.color:
                return True
    return False

def group3(self, board):
    """Alpha-Beta Pruning implementation"""
    if self.game.turn != self.color:
        return None, None

    def alpha_beta(board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.endGameCheck(board):
            return evaluate_board(board, self.color), None, None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for row, col, possible_moves in self.generatemove_at_a_time(board):
                for final_pos in possible_moves:
                    new_board = deepcopy(board)
                    new_board.move_piece(row, col, final_pos[0], final_pos[1])
                    
                    eval_score, _, _ = alpha_beta(new_board, depth-1, alpha, beta, False)
                    
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = ((row, col), final_pos)
                    
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            
            return max_eval, best_move[0] if best_move else None, best_move[1] if best_move else None
        else:
            min_eval = float('inf')
            best_move = None
            for row, col, possible_moves in self.generatemove_at_a_time(board):
                for final_pos in possible_moves:
                    new_board = deepcopy(board)
                    new_board.move_piece(row, col, final_pos[0], final_pos[1])
                    
                    eval_score, _, _ = alpha_beta(new_board, depth-1, alpha, beta, True)
                    
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = ((row, col), final_pos)
                    
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            
            return min_eval, best_move[0] if best_move else None, best_move[1] if best_move else None

    # Start alpha-beta search with depth 5
    _, current_pos, final_pos = alpha_beta(board, 5, float('-inf'), float('inf'), True)
    
    if current_pos and final_pos:
        if final_pos in board.get_valid_legal_moves(current_pos[0], current_pos[1], self.game.continue_playing):
            return current_pos, final_pos
            
    return None, None
