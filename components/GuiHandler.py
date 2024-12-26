import pygame, sys
from pygame.locals import *
from time import sleep

pygame.font.init()

WHITE    = (255, 255, 255)
GREY     = (128, 128, 128)
PURPLE      = (178, 102, 255)
BLACK    = (  0,   0,   0)
GOLD     = (51,0,51)
HIGH     = (160, 190, 255)


"""
The Board class represents the game board and the pieces on it. It has methods for initializing the board, checking for legal moves, and moving pieces.
It also has methods for checking whether a piece should be kinged and for removing pieces from the board.
"""

class Board:
	def __init__(self):
		self.matrix = self.create_board()

	def create_board(self):
		# Create a list of 8 rows, each containing 8 squares with the appropriate color
		# If the sum of the row and column indices is even, set the square color to white
		# If the sum of the row and column indices is odd, set the square color to black
		matrix = [[Square(WHITE) if (x + y) % 2 == 0 else Square(BLACK) for x in range(8)] for y in range(8)]

		# Place the purple and grey pieces on the appropriate squares
		# For each row and column of the matrix, check if the square is black and in the first three or last three rows
		# If the square meets these criteria, place a purple or grey piece on it, respectively
		for x in range(8):
			for y in range(3):
				if matrix[x][y].color == BLACK:
					matrix[x][y].squarePiece = Piece(PURPLE)
			for y in range(5, 8):
				if matrix[x][y].color == BLACK:
					matrix[x][y].squarePiece = Piece(GREY)

		# Return the completed matrix
		return matrix


	def remove_piece(self, x, y):
		captured_piece = self.matrix[x][y].squarePiece
		if captured_piece:
			print(f"[LOG] Piece taken from ({x},{y}) - Color: {captured_piece.color}")
		self.matrix[x][y].squarePiece = None

	def move_piece(self, start_x, start_y, end_x, end_y):

		self.matrix[end_x][end_y].squarePiece = self.matrix[start_x][start_y].squarePiece
		self.remove_piece(start_x, start_y)
		self.king(end_x, end_y)

	"""
	This method takes three arguments: the direction to move in (dir), and the current coordinates (x and y).
	The method then uses a series of if statements to determine the new coordinates based on the specified direction. 
	If the direction is valid, the method returns a tuple containing the new coordinates.
	If the direction is invalid, the method returns 0.
	"""
	def adjacent_square(self, dir, x, y):
		# If the direction is northwest, subtract 1 from both x and y to move to the new square
		if dir == "northwest":
			return (x - 1, y - 1)
		# If the direction is northeast, add 1 to x and subtract 1 from y to move to the new square
		elif dir == "northeast":
			return (x + 1, y - 1)
		# If the direction is southwest, subtract 1 from x and add 1 to y to move to the new square
		elif dir == "southwest":
			return (x - 1, y + 1)
		# If the direction is southeast, add 1 to both x and y to move to the new square
		elif dir == "southeast":
			return (x + 1, y + 1)
		# If the direction is invalid, return 0
		else:
			return 0

	# Return a list of the coordinates of the four squares adjacent to the one at (x,y)
	# The adjacent squares are obtained by calling the "rel" method with each of the four directions
	def getAdjacentSquares(self, x, y):
		return [self.adjacent_square("northwest", x, y), self.adjacent_square("northeast", x, y), self.adjacent_square("southwest", x, y), self.adjacent_square("southeast", x, y)]

	# Return the board square with those coordinates
	def getSquare(self, x, y):
		x = int(x)
		y = int(y)
		return self.matrix[x][y]

	"""
	If the piece is a grey non-king, the method returns a list of the two squares diagonally in front of it. 
	This is because grey pieces can only move diagonally forward. 
	If the piece is a purple non-king, the method returns a list of the two squares diagonally behind it. 
	This is because purple pieces can only move diagonally backward. 
	If the piece is a king, the method returns a list of all four adjacent squares, as kings can move in any direction diagonally.
	"""

	def get_legal_moves(self, x, y):
		if self.matrix[x][y].squarePiece != None:

			if self.matrix[x][y].squarePiece.king == False and self.matrix[x][y].squarePiece.color == GREY:
				blind_legal_moves = [self.adjacent_square("northwest", x, y), self.adjacent_square("northeast", x, y)]

			elif self.matrix[x][y].squarePiece.king == False and self.matrix[x][y].squarePiece.color == PURPLE:
				blind_legal_moves = [self.adjacent_square("southwest", x, y), self.adjacent_square("southeast", x, y)]

			else:
				blind_legal_moves = [self.adjacent_square("northwest", x, y), self.adjacent_square("northeast", x, y), self.adjacent_square("southwest", x, y), self.adjacent_square("southeast", x, y)]

		else:
			blind_legal_moves = []

		return blind_legal_moves

	def get_valid_legal_moves(self, x, y, continue_playing=False):
		# Get the blind legal moves for the specified square
		blind_legal_moves = self.get_legal_moves(x, y)

		# Initialize an empty list to store the valid legal moves
		legal_moves = []

		# If the player is not continuing a capture sequence
		if continue_playing == False:
			# Check each blind legal move
			for move in blind_legal_moves:
				# If the move is on the board
				if self.within_bounds(move[0], move[1]):
					# If the destination square is empty
					if self.getSquare(move[0], move[1]).squarePiece == None:
						# Add the move to the list of legal moves
						legal_moves.append(move)
					# If the destination square contains an enemy piece and the jump square is empty
					elif self.getSquare(move[0], move[1]).squarePiece.color != self.getSquare(x, y).squarePiece.color and self.within_bounds(move[0] + (move[0] - x), move[1] + (move[1] - y)) and self.getSquare(move[0] + (move[0] - x), move[1] + (move[1] - y)).squarePiece == None:
						# Add the jump move to the list of legalmoves
						legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		# If the player is continuing a capture sequence
		else:
			# Check each blind legal move
			for move in blind_legal_moves:
				# If the move is on the board and the destination square contains an enemy piece and the jump square is empty
				if self.within_bounds(move[0], move[1]) and self.getSquare(move[0], move[1]).squarePiece != None and self.getSquare(
						move[0], move[1]).squarePiece.color != self.getSquare(x, y).squarePiece.color and self.within_bounds(move[0] + (move[0] - x), move[1] + (move[1] - y)) and self.getSquare(move[0] + (move[0] - x), move[1] + (move[1] - y)).squarePiece == None:
					# Add the jump move to the list of legal moves
					legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

		# Return the list of legal moves
		return legal_moves

	def within_bounds(self, x, y):

		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


	def king(self, x, y):
		if self.getSquare(x, y).squarePiece != None:
			if (self.getSquare(x, y).squarePiece.color == GREY and y == 0) or (self.getSquare(x, y).squarePiece.color == PURPLE and y == 7):
				self.getSquare(x, y).squarePiece.crown()


class Piece:
	def __init__(self, color, king = False):
		self.color = color
		self.king = king
		self.value = 1

	def crown(self):
		self.king = True
		self.value = 2

"""
The Graphics class handles the display and user interface. It has methods for setting up the game window, updating the display, and drawing the board and pieces.
It also has a method for drawing messages to the screen.
"""

class Graphics:
	def __init__(self):
		self.caption = "Checkers"

		self.fps = 60
		self.clock = pygame.time.Clock()

		self.window_size = 600
		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.background = pygame.image.load('resources/board.png')

		self.square_size = self.window_size // 8
		self.piece_size = self.square_size // 2

		self.message = False

	def setup_window(self):
		pygame.init()
		pygame.display.set_caption(self.caption)


	def pixel_coords(self, board_coords):

		return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

	def board_coords(self, pixel_x, pixel_y):

		return (pixel_x // self.square_size, pixel_y // self.square_size)

	def highlight_squares(self, squares, origin):

		for square in squares:
			pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))

		if origin != None:
			pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

	def update_display(self, board, legal_moves, selected_piece):

		# Extended window size to accommodate sideboard
		if self.screen.get_width() == self.window_size:
			self.screen = pygame.display.set_mode((self.window_size + 200, self.window_size))

		self.screen.blit(self.background, (0,0))

		self.highlight_squares(legal_moves, selected_piece)
		self.draw_board_pieces(board)

		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		# Draw sideboard with current scores and probabilities
		# For demonstration, use the values from the main Game instance if needed
		# In real usage, pass them as parameters or store them globally
		if hasattr(pygame, 'game_instance'):  # Just an example approach
			g = pygame.game_instance
			self.draw_sideboard(g.purple_score, g.grey_score, g.purple_prob, g.grey_prob)
			print(g.purple_score, g.grey_score, g.purple_prob, g.grey_prob)
		else:
			self.draw_sideboard(0, 0, 50, 50)

		pygame.display.update()
		self.clock.tick(self.fps)

	def draw_board_squares(self, board):

		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )

	def draw_board_pieces(self, board):

		for x in range(8):
			for y in range(8):
				if board.matrix[x][y].squarePiece != None:
					pygame.draw.circle(self.screen, board.matrix[x][y].squarePiece.color, tuple(map(int, self.pixel_coords((x, y)))), int(self.piece_size))

					if board.getSquare(x, y).squarePiece.king == True:
						pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x, y)), int(self.piece_size // 1.7), self.piece_size // 4)

	def draw_sideboard(self, purple_score, grey_score, purple_prob, grey_prob):
		# Simple sideboard rectangle on the right
		sideboard_x = self.window_size
		sideboard_width = 200
		pygame.draw.rect(self.screen, (50, 50, 50), (sideboard_x, 0, sideboard_width, self.window_size))
		font = pygame.font.SysFont(None, 24)

		# Display scores
		purple_text = font.render(f"Purple Score: {purple_score}", True, (255,255,255))
		grey_text = font.render(f"Grey Score: {grey_score}", True, (255,255,255))
		self.screen.blit(purple_text, (sideboard_x + 10, 50))
		self.screen.blit(grey_text, (sideboard_x + 10, 80))

		# Simple horizontal progress bar
		bar_y = 150
		bar_height = 20
		pygame.draw.rect(self.screen, (255, 255, 255), (sideboard_x + 10, bar_y, sideboard_width - 20, bar_height), 2)
		# Purple portion
		purple_bar_width = int((purple_prob / 100) * (sideboard_width - 20))
		pygame.draw.rect(self.screen, PURPLE, (sideboard_x + 10, bar_y, purple_bar_width, bar_height))
		# Grey portion (draw from the right side)
		grey_bar_width = (sideboard_width - 20) - purple_bar_width
		pygame.draw.rect(self.screen, GREY, (sideboard_x + 10 + purple_bar_width, bar_y, grey_bar_width, bar_height))



	def draw_message(self, message):
		"""
		Draws message to the screen.
		"""
		self.message = True
		self.font_obj = pygame.font.Font('resources/ChrustyRock-ORLA.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size // 2, self.window_size // 2)




# Used to create matrix
class Square:
	def __init__(self, color, squarePiece = None):
		self.color = color # color of board square
		self.squarePiece = squarePiece


"""
The Game class controls the overall game flow,which has several methods for setting up the game,
updating the game state, and terminating the game. It also has a main method that runs the game loop.
"""


class Game:

	def __init__(self, loop_mode):
		self.graphics = Graphics()
		self.board = Board()
		self.endGame = False
		self.turn = GREY
		self.selected_piece = None
		self.continue_playing = False
		self.loop_mode = loop_mode
		self.selected_legal_moves = []
		self.purple_score = 0
		self.grey_score = 0
		self.purple_prob = 50
		self.grey_prob = 50
		self.purple_captures = 0
		self.grey_captures = 0

	def setup(self):
		self.graphics.setup_window()

	def update(self):
		self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

	def terminate_game(self):
		pygame.quit()
		sys.exit()

	def main(self):
		self.setup()
		pygame.game_instance = self  # Set the game instance for access in Graphics
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False
				elif event.type == MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()
					board_pos = self.graphics.board_coords(x, y)

					if self.selected_piece is None:
						# Select piece if it belongs to current player
						piece = self.board.getSquare(board_pos[0], board_pos[1]).squarePiece
						if piece and piece.color == self.turn:
							self.selected_piece = board_pos
							self.selected_legal_moves = self.board.get_valid_legal_moves(
								board_pos[0], board_pos[1], self.continue_playing
							)
					else:
						# If user clicked on a valid destination
						if board_pos in self.selected_legal_moves:
							self.board.move_piece(
								self.selected_piece[0], self.selected_piece[1],
								board_pos[0], board_pos[1]
							)

							# If it was a capture, remove the piece in between & allow chaining
							if board_pos not in self.board.getAdjacentSquares(
									self.selected_piece[0], self.selected_piece[1]):
								capture_x = self.selected_piece[0] + (board_pos[0] - self.selected_piece[0]) // 2
								capture_y = self.selected_piece[1] + (board_pos[1] - self.selected_piece[1]) // 2
								self.board.remove_piece(capture_x, capture_y)

								# Log capture & update score/probability
								self.update_scores_and_probability(self.turn)

								# Look for another capture
								new_moves = self.board.get_valid_legal_moves(board_pos[0], board_pos[1], True)
								if new_moves:
									self.selected_piece = board_pos
									self.selected_legal_moves = new_moves
									self.continue_playing = True
									continue
							# If no further capture, end turn
							self.end_turn()
						else:
							# If clicked invalid destination or new piece
							self.selected_piece = None
							self.selected_legal_moves = []
			self.update()
			if self.endGame:
				running = False
		self.terminate_game()

	def end_turn(self):
		if self.turn == GREY:
			self.turn = PURPLE
		else:
			self.turn = GREY

		self.selected_piece = None
		self.selected_legal_moves = []
		self.continue_playing = False

		if self.check_for_endgame():
			if self.turn == GREY:
				self.graphics.draw_message("PURPLE WINS!")
			else:
				self.graphics.draw_message("GREY WINS!")
			if(self.loop_mode):
				self.endGame = True
			else:
				self.terminate_game()

	def check_for_endgame(self):
		for x in range(8):
			for y in range(8):
				if self.board.getSquare(x, y).color == BLACK and self.board.getSquare(x, y).squarePiece != None and self.board.getSquare(x, y).squarePiece.color == self.turn:
					if self.board.get_valid_legal_moves(x, y) != []:
						return False

		return True
	
	def calculate_scores(self):
		purple_pieces = grey_pieces = 0
		purple_kings = grey_kings = 0
		
		# Count current pieces and kings
		for x in range(8):
			for y in range(8):
				piece = self.board.getSquare(x, y).squarePiece
				if piece:
					if piece.color == PURPLE:
						purple_pieces += 1
						if piece.king:
							purple_kings += 1
							pos = (x, y)
							if pos not in self.kings['purple']:
								self.kings['purple'].add(pos)
								self.current_score['purple'] += 50  # Bonus for new king
					else:
						grey_pieces += 1
						if piece.king:
							grey_kings += 1
							pos = (x, y)
							if pos not in self.kings['grey']:
								self.kings['grey'].add(pos)
								self.current_score['grey'] += 50  # Bonus for new king
		# Update scores (8 points per piece)
		self.purple_score = purple_pieces * 8 + len(self.kings['purple']) * 50 + self.captured_pieces['purple'] * 8
		self.grey_score = grey_pieces * 8 + len(self.kings['grey']) * 50 + self.captured_pieces['grey'] * 8
		# Calculate probabilities based on piece count and position
		total_pieces = max(purple_pieces + grey_pieces, 1)
		base_purple_prob = (purple_pieces / total_pieces) * 100
		base_grey_prob = (grey_pieces / total_pieces) * 100
		# Adjust probabilities based on kings and captures
		king_factor = (purple_kings - grey_kings) * 5
		capture_factor = (self.captured_pieces['purple'] - self.captured_pieces['grey']) * 2
		# Calculate final probabilities (rounded to nearest integer)
		self.purple_prob = min(max(int(base_purple_prob + king_factor + capture_factor), 5), 95)
		self.grey_prob = 100 - self.purple_prob
	def calculate_position_bonus(self):
		bonus = 0
		for x in range(8):
			for y in range(8):
				piece = self.board.getSquare(x, y).squarePiece
				if piece:
					if piece.color == PURPLE:
						if y > 4:  # Advanced position
							bonus += 0.1
						if piece.king and y > 5:  # Advanced king
							bonus += 0.2
					else:
						if y < 3:  # Advanced position
							bonus -= 0.1
						if piece.king and y < 2:  # Advanced king
							bonus -= 0.2
		return max(min(bonus, 1), -1)  # Normalize between -1 and 1
	def update_capture(self, capturing_color):
		self.captured_pieces[capturing_color.lower()] += 1
		self.current_score[capturing_color.lower()] += 8  # 8 points for

	def update_scores_and_probability(self, capturing_color):
		 # Use captures to track how many pieces each side has taken
		if capturing_color == PURPLE:
			self.purple_captures += 1
		else:
			self.grey_captures += 1

		# Recount how many pieces each side still has
		purple_pieces = 0
		grey_pieces = 0
		for x in range(8):
			for y in range(8):
				piece = self.board.getSquare(x, y).squarePiece
				if piece:
					if piece.color == PURPLE:
						purple_pieces += 1
					else:
						grey_pieces += 1

		# Final score = pieces on board + captures×8
		self.purple_score = self.purple_captures * 8
		self.grey_score = self.grey_captures * 8

		# Probability = ratio of scores
		total = max(self.purple_score + self.grey_score, 1)
		self.purple_prob = int((self.purple_score / total) * 100)
		self.grey_prob = 100 - self.purple_prob
		print(f"[LOG] Scores => Purple: {self.purple_score}, Grey: {self.grey_score}")
		print(f"[LOG] Probability => Purple: {self.purple_prob}%, Grey: {self.grey_prob}%")
