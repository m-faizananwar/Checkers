from copy import deepcopy
import random
PURPLE = (178, 102, 255)

def evaluate_position(board, color):
    purple_score = grey_score = 0
    for x in range(8):
        for y in range(8):
            piece = board.getSquare(x, y).squarePiece
            if piece:
                # Base piece value
                value = 10
                # Position value
                if piece.color == PURPLE:
                    value += y * 1.2  # Favor forward movement
                    if 2 <= x <= 5:  # Center control bonus
                        value += 2
                    purple_score += value
                else:
                    value += (7-y) * 1.2
                    if 2 <= x <= 5:
                        value += 2
                    grey_score += value
                    
    return purple_score - grey_score if color == PURPLE else grey_score - purple_score

def expectimax(self, board, depth, maximizing_player):
    if depth == 0 or self.endGameCheck(board):
        return evaluate_position(board, self.color), None, None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        moves = list(self.generatemove_at_a_time(board))
        
        for row, col, possible_moves in moves:
            for final_pos in possible_moves:
                new_board = deepcopy(board)
                new_board.move_piece(row, col, final_pos[0], final_pos[1])
                
                eval_score, _, _ = expectimax(self, new_board, depth-1, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = ((row, col), final_pos)
        
        return max_eval, best_move[0] if best_move else None, best_move[1] if best_move else None
    else:
        # Chance node - average all possible outcomes
        total_eval = 0
        count = 0
        moves = list(self.generatemove_at_a_time(board))
        
        for row, col, possible_moves in moves:
            for final_pos in possible_moves:
                new_board = deepcopy(board)
                new_board.move_piece(row, col, final_pos[0], final_pos[1])
                
                eval_score, _, _ = expectimax(self, new_board, depth-1, True)
                total_eval += eval_score
                count += 1
        
        # Return average score for chance nodes
        return (total_eval / count) if count > 0 else 0, None, None

def group4(self, board):
    """Expectimax implementation"""
    if self.game.turn != self.color:
        return None, None

    _, current_pos, final_pos = expectimax(self, board, 4, True)
    
    if current_pos and final_pos:
        if final_pos in board.get_valid_legal_moves(current_pos[0], current_pos[1], self.game.continue_playing):
            return current_pos, final_pos
            
    return None, None
