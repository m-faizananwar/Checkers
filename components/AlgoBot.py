import pygame
from pygame.locals import *
from copy import deepcopy
import math
pygame.font.init()

from group1 import group1
from group2 import group2

GREY = (128, 128, 128)
PURPLE = (178, 102, 255)
BLACK = (0,   0,   0)

class Bot:
    def __init__(self, game, color, method='random', depth=1):
        # Initialize the attributes of the Player object
        self.method = method
        self.mid_phase = self.evaluate  # Set the evaluation function for the mid-game phase
        self.end_phase = self.evaluateDistance  # Set the evaluation function for the end-game phase
        self.depth = depth  # Set the depth of the algorithm
        self.game = game  # Set the Game object that the Player is playing
        self.color = color  # Set the color of the Player's pieces
        self.eval_color = color  # Set the color used for evaluation (initially set to the Player's color)
        if self.color == GREY:
            self.opponent_color = PURPLE  # Set the color of the opponent's pieces
        else:
            self.opponent_color = GREY  # Set the color of the opponent's pieces
        self._current_eval = self.mid_phase  # Initialize the current evaluation function to the mid-game evaluation
        self._end_eval_time = False  # Initialize the end-game evaluation time to False

    def iskings(self, board):
        # Check if all pieces on the board are kings
        for i in range(8):
            for j in range(8):
                squarePiece = board.getSquare(i, j).squarePiece
                if squarePiece is not None and squarePiece.king == False:
                    return False
        return True

    def distance(self, x1, y1, x2, y2):
        # Calculate the Euclidean distance between two points
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    """
    The step method checks if the game has entered the end phase, and if so, evaluates the current board state.
    It then calls the appropriate move method based on the method attribute of the class instance.
    """
    def step(self, board):
        if self.end_phase is not None and self._end_eval_time == False:
            if self.iskings(board):
                self._end_eval_time = True
                self._current_eval = self.end_phase
        if self.method == 'group1':
            self.group1(board)
        elif self.method == 'group2':
            self.group2(board)

    def getPossibleMoves(self, board):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if(board.get_valid_legal_moves(i, j, self.game.continue_playing) != [] and board.getSquare(i, j).squarePiece != None and board.getSquare(i, j).squarePiece.color == self.game.turn):
                    possible_moves.append((i, j, board.get_valid_legal_moves(i, j, self.game.continue_playing)))
        return possible_moves

    def generatemove_at_a_time(self, board):
        for i in range(8):
            for j in range(8):
                if(board.get_valid_legal_moves(i, j, self.game.continue_playing) != [] and board.getSquare(i, j).squarePiece != None and board.getSquare(i, j).squarePiece.color == self.game.turn):
                    yield (i, j, board.get_valid_legal_moves(i, j, self.game.continue_playing))

    
    def group1(self,board):
        random_move, random_choice = group1(self,board)
        self.move(random_move, random_choice, board)
        return
    
    def group2(self,board):
        random_move, random_choice = group2(self,board)
        self.move(random_move, random_choice, board)
        return
    

    def move(self, current_pos, final_pos, board):
        # If the current position is None, end the turn
        if current_pos is None:
            self.game.end_turn()

        # If the game is over, check if the final position is occupied by a friendly piece
        if self.game.continue_playing == False:
            if board.getSquare(final_pos[0], final_pos[1]).squarePiece is not None and board.getSquare(final_pos[0],
                                                                                                       final_pos[
                                                                                                           1]).squarePiece.color == self.game.turn:
                # If it is, update the current position
                current_pos = final_pos

            # Otherwise, if the final position is a valid legal move from the current position, make the move
            elif current_pos != None and final_pos in board.get_valid_legal_moves(current_pos[0], current_pos[1]):
                board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                # If the move is a capture, remove the captured piece and allow the player to continue making moves
                if final_pos not in board.getAdjacentSquares(current_pos[0], current_pos[1]):
                    board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                       2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)
                    self.game.continue_playing = True

                # Update the current position and check if the player can make another move
                current_pos = final_pos
                final_pos = board.get_valid_legal_moves(
                    current_pos[0], current_pos[1], True)
                if final_pos != []:
                    self.move(current_pos, final_pos[0], board)

                # End the turn
                self.game.end_turn()

        # If the player can continue making moves, check if the final position is a valid legal move
        if self.game.continue_playing == True:
            if current_pos != None and final_pos in board.get_valid_legal_moves(current_pos[0], current_pos[1],
                                                                                self.game.continue_playing):
                board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                # If the move is a capture, remove the captured piece
                board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                   2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

            # Check if the player can make another move or if the turn should end
            if board.get_valid_legal_moves(final_pos[0], final_pos[1], self.game.continue_playing) == []:
                self.game.end_turn()
            else:
                # Update the current position and check if the player can make another move
                current_pos = final_pos
                final_pos = board.get_valid_legal_moves(
                    current_pos[0], current_pos[1], True)
                if final_pos != []:
                    self.move(current_pos, final_pos[0], board)

                # End the turn
                self.game.end_turn()

        # If the game is over, switch to the opponent's turn
        if self.game.continue_playing != True:
            self.game.turn = self.opponent_color

    def moveOnBoard(self, board, current_pos, final_pos, continue_playing=False):
        # If continue_playing is False, check if the final position is occupied by a friendly piece
        if continue_playing == False:
            if board.getSquare(final_pos[0], final_pos[1]).squarePiece != None and board.getSquare(final_pos[0],
                                                                                                   final_pos[1]).squarePiece.color == self.game.turn:
                # If it is, update the current position
                current_pos = final_pos

            # Otherwise, if the final position is a valid legal move from the current position, make the move
            elif current_pos != None and final_pos in board.get_valid_legal_moves(current_pos[0], current_pos[1]):
                board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                # If the move is a capture, remove the captured piece and allow the player to continue making moves
                if final_pos not in board.getAdjacentSquares(current_pos[0], current_pos[1]):
                    board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                       2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)
                    continue_playing = True

                # Update the current position and# If continue_playing is False, check if the final position is occupied by a friendly piece
                current_pos = final_pos
                final_pos = board.get_valid_legal_moves(current_pos[0], current_pos[1], True)
                if final_pos != []:
                    # Recursively call moveOnBoard with the new final_pos and continue_playing set to True
                    self.moveOnBoard(board, current_pos, final_pos[0], continue_playing=True)

        # If continue_playing is True, check if the final position is a valid legal move
        else:
            if current_pos != None and final_pos in board.get_valid_legal_moves(current_pos[0], current_pos[1],continue_playing):
                board.move_piece(current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                # If the move is a capture, remove the captured piece
                board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) // 2,
                                   current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

            # Check if the player can make another move or if the turn should end
            if board.get_valid_legal_moves(final_pos[0], final_pos[1], self.game.continue_playing) == []:
                return
            else:
                # Update the current position and recursively call moveOnBoard with the new final_pos and continue_playing set to True
                current_pos = final_pos
                final_pos = board.get_valid_legal_moves(current_pos[0], current_pos[1], True)
                if final_pos != []:
                    self.moveOnBoard(board, current_pos, final_pos[0], continue_playing=True)

    

    def evaluate(self, board):
        score = 0
        num_pieces = 0
        # Evaluate the board position based on the current player's color
        if (self.eval_color == PURPLE):
            for i in range(8):
                for j in range(8):
                    squarePiece = board.getSquare(i, j).squarePiece
                    if (squarePiece is not None):
                        num_pieces += 1
                        # Evaluate the score based on the type and position of the piece
                        if squarePiece.color == self.eval_color and squarePiece.king:
                            score += 10
                        elif squarePiece.color != self.eval_color and squarePiece.king:
                            score -= 10
                        elif squarePiece.color == self.eval_color and j < 4:
                            score += 5
                        elif squarePiece.color != self.eval_color and j < 4:
                            score -= 7
                        elif squarePiece.color == self.eval_color and j >= 4:
                            score += 7
                        elif squarePiece.color != self.eval_color and j >= 4:
                            score -= 5
        else:
            for i in range(8):
                for j in range(8):
                    squarePiece = board.getSquare(i, j).squarePiece
                    if (squarePiece is not None):
                        num_pieces += 1
                        # Evaluate the score based on the type and position of the piece
                        if squarePiece.color == self.eval_color and squarePiece.king:
                            score += 10
                        elif squarePiece.color != self.eval_color and squarePiece.king:
                            score -= 10
                        elif squarePiece.color == self.eval_color and j < 4:
                            score += 7
                        elif squarePiece.color != self.eval_color and j < 4:
                            score -= 5
                        elif squarePiece.color == self.eval_color and j >= 4:
                            score += 7
                        elif squarePiece.color != self.eval_color and j >= 4:
                            score -= 5
        # Return the average score per piece on the board
        return score / num_pieces

    def allPiecesLocation(self, board):
        """
        Returns the locations of all pieces on the board for the current player and the opponent.

        Parameters:
        board (Board): The current state of the game board.

        Returns:
        tuple: A tuple of two lists, one containing the locations of the current player's pieces and one containing
               the locations of the opponent's pieces.
        """
        # Initialize empty lists to store the locations of the current player's pieces and the opponent's pieces.
        player_pieces = []
        opponent_pieces = []

        # Iterate over each square on the board.
        for i in range(8):
            for j in range(8):
                # Get the piece on the current square, if any.
                squarePiece = board.getSquare(i, j).squarePiece
                if (squarePiece is not None):
                    # If there is a piece on the current square, add its location to the appropriate list
                    # based on its color.
                    if (squarePiece.color == self.eval_color):
                        player_pieces.append((i, j))
                    else:
                        opponent_pieces.append((i, j))

        # Return a tuple containing the lists of the current player's pieces and the opponent's pieces.
        return player_pieces, opponent_pieces

    def evaluateDistance(self, board):
        # Calculate the sum of distances between all player pieces and opponent pieces on the board
        player_pieces, adversary_pieces = self.allPiecesLocation(board)
        sum_of_dist = 0
        for pos in player_pieces:
            for adv in adversary_pieces:
                sum_of_dist += self.distance(pos[0], pos[1], adv[0], adv[1])
        # If the player has more pieces than the opponent, negate the sum of distances
        if (len(player_pieces) >= len(adversary_pieces)):
            sum_of_dist *= -1
        return sum_of_dist

    # Determine whether the current board position corresponds to an endgame phase
    def endGameCheck(self, board):
        # Iterate over every square on the board
        for x in range(8):
            for y in range(8):
                # Check whether the square is occupied by a piece of the player whose turn it is
                if board.getSquare(x, y).color == BLACK and board.getSquare(x,y).squarePiece is not None and board.getSquare(x, y).squarePiece.color == self.game.turn:
                    # Check whether the piece has any legal moves available
                    if board.get_valid_legal_moves(x, y) != []:
                        # If the piece has legal moves available, the game is not in an endgame phase
                        return False
        # If no player piece has legal moves available, the game is in an endgame phase
        return True
