import random

def group2(self, board):
    if self.game.turn != self.color:  # Only move if it's this AI's turn
        return None

    possible_moves = self.getPossibleMoves(board)
    if not possible_moves:
        return None
        
    random_move = random.choice(possible_moves)
    rand_choice = random.choice(random_move[2])
    
    # Validate move
    if rand_choice in board.get_valid_legal_moves(random_move[0], random_move[1], self.game.continue_playing):
        return random_move, rand_choice
    return None
