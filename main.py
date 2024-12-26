# Import the Game class from the GuiHandler module and the Bot class from the gamebot module---
from PyQt5.QtGui import QPixmap, QBrush, QPalette
from pygame import *
import pygame
from components.GuiHandler import Game
from components.AlgoBot import Bot

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, \
    QDesktopWidget

# Import the sleep function from the time module
from time import sleep
import time
from PyQt5.QtCore import Qt

# Define the colors blue and red in RGB format
GREY = (128, 128, 128)
PURPLE = (178, 102, 255)
# Define a function to play the game
def play_game(Method1,Method2):
    game = Game(loop_mode=True)
    pygame.game_instance = game  # Set the game instance for access in Graphics
    game.setup()
    purple_bot = Bot(game, PURPLE, method=Method1)
    grey_bot = Bot(game, GREY, method=Method2)
    start_time = time.time()

    # Enter the main game loop, where each bot takes turns until the game is over
    while not game.endGame:
        if game.turn == GREY:
            grey_bot.step(game.board)
        else:
            purple_bot.step(game.board)
        game.update()
        sleep(0.0999)   # Add a delay between turns
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    sleep(2)

def play_game_player_vs_player():
    game = Game(loop_mode=False)
    game.main()

def play_game_player_vs_ai(ai_method):
    game = Game(loop_mode=True)
    pygame.game_instance = game  # Set the game instance for access in Graphics
    game.setup()
    ai_color = PURPLE  # AI controls Purple
    bot = Bot(game, ai_color, method=ai_method)
    running = True

    while not game.endGame and running:
        if game.turn == ai_color:
            bot.step(game.board)
            game.update()
            sleep(0.0999)
        else:  # Player's turn
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN and game.turn != ai_color:  # Only allow moves on player's turn
                    x, y = pygame.mouse.get_pos()
                    board_pos = game.graphics.board_coords(x, y)
                    if game.selected_piece is None:
                        piece = game.board.getSquare(board_pos[0], board_pos[1]).squarePiece
                        if piece and piece.color == game.turn:
                            game.selected_piece = board_pos
                            game.selected_legal_moves = game.board.get_valid_legal_moves(
                                board_pos[0], board_pos[1], game.continue_playing
                            )
                    else:
                        if board_pos in game.selected_legal_moves:
                            game.board.move_piece(
                                game.selected_piece[0], game.selected_piece[1],
                                board_pos[0], board_pos[1]
                            )
                            if board_pos not in game.board.getAdjacentSquares(
                                    game.selected_piece[0], game.selected_piece[1]):
                                capture_x = game.selected_piece[0] + (board_pos[0] - game.selected_piece[0]) // 2
                                capture_y = game.selected_piece[1] + (board_pos[1] - game.selected_piece[1]) // 2
                                game.board.remove_piece(capture_x, capture_y)
                                game.update_scores_and_probability(game.turn)  # Update scores and probability
                                new_moves = game.board.get_valid_legal_moves(board_pos[0], board_pos[1], True)
                                if new_moves:
                                    game.selected_piece = board_pos
                                    game.selected_legal_moves = new_moves
                                    game.continue_playing = True
                                    continue
                            game.end_turn()
                        else:
                            game.selected_piece = None
                            game.selected_legal_moves = []
        game.update()
        sleep(0.0999)
    sleep(2)

def play_game_ai_vs_ai(Method1, Method2):
    # Reuse existing logic from play_game(Method1, Method2)
    play_game(Method1, Method2)

class GameTypeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Select Game Type')
        screen = QDesktopWidget().screenGeometry()
        center_x, center_y = screen.width() / 2, screen.height() / 2
        self.setGeometry(0, 0, 800, 500)
        top_left_x = int(center_x - (self.width() / 2)) - 100
        top_left_y = int(center_y - (self.height() / 2)) - 100
        self.move(top_left_x, top_left_y)

        palette = QPalette()
        background_image = QPixmap('resources/background.jpg')
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.setPalette(palette)

        main_layout = QVBoxLayout()

        # Add row with bot images
        row_layout = QHBoxLayout()
        purple_label = QLabel()
        purple_label.setPixmap(QPixmap('resources/purpleBot.png'))
        grey_label = QLabel()
        grey_label.setPixmap(QPixmap('resources/greyBot.png'))
        row_layout.addWidget(purple_label)
        vs_label = QLabel("VS")
        vs_label.setStyleSheet('font-size: 40px; color: #FFFFFF; font-weight: bold;')
        row_layout.addWidget(vs_label)
        row_layout.addWidget(grey_label)
        main_layout.addLayout(row_layout)

        # Buttons for selecting game type
        btn_pvp = QPushButton("Player vs Player")
        btn_pvp.setFixedSize(300, 60)
        btn_pvp.clicked.connect(self.pvp_clicked)

        btn_pvai = QPushButton("Player vs AI")
        btn_pvai.setFixedSize(300, 60)
        btn_pvai.clicked.connect(self.pvai_clicked)

        btn_aivai = QPushButton("AI vs AI")
        btn_aivai.setFixedSize(300, 60)
        btn_aivai.clicked.connect(self.aivai_clicked)

        main_layout.addStretch(1)
        for b in [btn_pvp, btn_pvai, btn_aivai]:
            b.setStyleSheet("font-size:18px; color:white; background-color:#9933ff;")
            main_layout.addWidget(b, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def pvp_clicked(self):
        self.close()
        play_game_player_vs_player()

    def pvai_clicked(self):
        self.close()
        self.ms_window = MethodSelectionWindowSingle()
        self.ms_window.show()

    def aivai_clicked(self):
        self.close()
        self.md_window = MethodSelectionWindowDouble()
        self.md_window.show()

class MethodSelectionWindowSingle(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Select AI Method')
        screen = QDesktopWidget().screenGeometry()
        center_x, center_y = screen.width() / 2, screen.height() / 2
        self.setGeometry(0, 0, 800, 500)
        top_left_x = int(center_x - (self.width() / 2)) - 100
        top_left_y = int(center_y - (self.height() / 2)) - 100
        self.move(top_left_x, top_left_y)

        palette = QPalette()
        background_image = QPixmap('resources/background.jpg')
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.setPalette(palette)

        main_layout = QVBoxLayout()

        # Row with bot images
        player_row = QHBoxLayout()
        computer_photo = QLabel()
        computer_photo.setPixmap(QPixmap('resources/purpleBot.png'))
        player_row.addWidget(computer_photo)

        label = QLabel('VS')
        label.setStyleSheet('font-size: 40px; color: #FFFFFF')
        label_font = label.font()
        label_font.setBold(True)
        label.setFont(label_font)
        player_row.addWidget(label)

        agent_photo = QLabel()
        agent_photo.setPixmap(QPixmap('resources/greyBot.png'))
        player_row.addWidget(agent_photo)

        main_layout.addLayout(player_row)

        # Second row (purple bot info on left, “human” on right or just label)
        player_row2 = QHBoxLayout()
        # Purple side
        computer_column = QVBoxLayout()
        computer_label = QLabel('                        Purple Bot')
        computer_label.setStyleSheet('color: #FFFFFF')
        comp_font = computer_label.font()
        comp_font.setBold(True)
        comp_font.setPointSize(15)
        computer_label.setFont(comp_font)
        computer_column.addWidget(computer_label)

        algorithm_label = QLabel('Choose algorithm:')
        algorithm_label.setStyleSheet('font-size:16px; color:#FFFFFF')
        self.algorithm_combo = QComboBox()
        # Update with difficulty labels
        self.algorithm_choices = {
            'Easy (Random)': 'group2',
            'Medium (Minimax)': 'group1',
            'Hard (Alpha-Beta)': 'group3',
            'Extra Hard (Expectimax)': 'group4'
        }
        self.algorithm_combo.addItems(list(self.algorithm_choices.keys()))
        self.algorithm_combo.setStyleSheet('color:black')
        self.algorithm_combo.setFixedSize(500, 40)
        computer_column.addWidget(algorithm_label)
        computer_column.addWidget(self.algorithm_combo)
        player_row2.addLayout(computer_column)

        # Grey side
        # You could leave it as “Player” or “Human,” or simply show a label
        agent_column = QVBoxLayout()
        agent_label = QLabel('                          Player')
        agent_label.setStyleSheet('color: #FFFFFF; font-size:15px; font-weight:bold;')
        agent_column.addWidget(agent_label)
        player_row2.addLayout(agent_column)

        main_layout.addLayout(player_row2)

        # Play button
        submit_button = QPushButton('Play')
        submit_button.setStyleSheet('''
            QPushButton {
                background-color: #9933ff;
                border: 2px solid #9933ff;
                color: white;
                font-size: 24px;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f00ff;
                border: 2px solid #7f00ff;
            }
        ''')
        submit_button.clicked.connect(self.start_game)
        main_layout.addWidget(submit_button)

        self.setLayout(main_layout)

    def start_game(self):
        selected_text = self.algorithm_combo.currentText()
        ai_method = self.algorithm_choices[selected_text]
        self.close()
        play_game_player_vs_ai(ai_method)

class MethodSelectionWindowDouble(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Select AI Methods')
        # ...same geometry and palette code...
        screen = QDesktopWidget().screenGeometry()
        # ...existing code for positioning...
        palette = QPalette()
        background_image = QPixmap('resources/background.jpg')
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.setPalette(palette)

        main_layout = QVBoxLayout()

        # Row with bot images
        player_row = QHBoxLayout()
        computer_photo = QLabel()
        computer_photo.setPixmap(QPixmap('resources/purpleBot.png'))
        player_row.addWidget(computer_photo)

        label = QLabel('VS')
        label.setStyleSheet('font-size: 40px; color: #FFFFFF')
        label_font = label.font()
        label_font.setBold(True)
        label.setFont(label_font)
        player_row.addWidget(label)

        agent_photo = QLabel()
        agent_photo.setPixmap(QPixmap('resources/greyBot.png'))
        player_row.addWidget(agent_photo)

        main_layout.addLayout(player_row)

        # Second row (both columns have combos)
        player_row2 = QHBoxLayout()
        # Purple side
        computer_column = QVBoxLayout()
        computer_label = QLabel('                        Purple Bot')
        computer_label.setStyleSheet('color: #FFFFFF; font-size:15px; font-weight:bold;')
        computer_column.addWidget(computer_label)

        algorithm_label = QLabel('Choose algorithm:')
        algorithm_label.setStyleSheet('font-size:16px; color:#FFFFFF')
        self.algorithm_choices = {
            'Easy (Random)': 'group2',
            'Medium (Minimax)': 'group1',
            'Hard (Alpha-Beta)': 'group3',
            'Extra Hard (Expectimax)': 'group4'
        }
        
        # Purple bot combo
        self.algorithm_combo_purple = QComboBox()
        self.algorithm_combo_purple.addItems(list(self.algorithm_choices.keys()))
        self.algorithm_combo_purple.setStyleSheet('color:black')
        self.algorithm_combo_purple.setFixedSize(500, 40)

        computer_column.addWidget(algorithm_label)
        computer_column.addWidget(self.algorithm_combo_purple)
        player_row2.addLayout(computer_column)

        # Grey side
        agent_column = QVBoxLayout()
        agent_label = QLabel('                          Grey Bot')
        agent_label.setStyleSheet('color:#FFFFFF; font-size:15px; font-weight:bold;')
        agent_column.addWidget(agent_label)

        algorithm_label1 = QLabel('Choose algorithm:')
        algorithm_label1.setStyleSheet('font-size:16px; color:#FFFFFF')
        self.algorithm_combo_grey = QComboBox()
        self.algorithm_combo_grey.addItems(list(self.algorithm_choices.keys()))
        self.algorithm_combo_grey.setStyleSheet('color:black')
        self.algorithm_combo_grey.setFixedSize(500, 40)
        agent_column.addWidget(algorithm_label1)
        agent_column.addWidget(self.algorithm_combo_grey)

        player_row2.addLayout(agent_column)
        main_layout.addLayout(player_row2)

        # Play button
        submit_button = QPushButton('Play')
        submit_button.setStyleSheet('''
            QPushButton {
                background-color: #9933ff;
                border: 2px solid #9933ff;
                color: white;
                font-size: 24px;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f00ff;
                border: 2px solid #7f00ff;
            }
        ''')
        submit_button.clicked.connect(self.start_game)
        main_layout.addWidget(submit_button)

        self.setLayout(main_layout)

    def start_game(self):
        purple_text = self.algorithm_combo_purple.currentText()
        grey_text = self.algorithm_combo_grey.currentText()
        method1 = self.algorithm_choices[purple_text]
        method2 = self.algorithm_choices[grey_text]
        self.close()
        play_game_ai_vs_ai(method1, method2)

# Update the main entry point:
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameTypeWindow()
    window.show()
    sys.exit(app.exec_())