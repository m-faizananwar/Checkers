# Import the Game class from the GuiHandler module and the Bot class from the gamebot module---
from PyQt5.QtGui import QPixmap, QBrush, QPalette

from components.GuiHandler import Game
from components.AlgoBot import Bot

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, \
    QDesktopWidget

# Import the sleep function from the time module
from time import sleep
import time

# Define the colors blue and red in RGB format
GREY = (128, 128, 128)
PURPLE = (178, 102, 255)
# Define a function to play the game
def play_game(Method1,Method2):
    # Create a new game object and set it up for play
    game = Game(loop_mode=True)
    game.setup()
    # Create a red bot and a blue bot with their respective evaluation methods and search algorithms
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

class CheckersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome to Checkers!')
        screen = QDesktopWidget().screenGeometry()
        center_x, center_y = screen.width() /2, screen.height() /2
        self.setGeometry(0, 0, 800, 500)

        # Calculate the top-left point
        top_left_x = int(center_x - (self.width() / 2))
        top_left_y = int(center_y - (self.height() / 2))

        # Move the window to the top-left point
        self.move(top_left_x, top_left_y)

        palette = QPalette()
        background_image = QPixmap('resources/background.jpg')
        palette.setBrush(QPalette.Background, QBrush(background_image))
        self.setPalette(palette)

        main_layout = QVBoxLayout()

        # Add player photos
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

        # Add player information
        player_row2 = QHBoxLayout()
        computer_column = QVBoxLayout()
        computer_label = QLabel('                        Purple Bot')
        computer_label.setStyleSheet('color: #FFFFFF')
        computer_label_font = computer_label.font()
        computer_label_font.setBold(True)
        computer_label_font.setPointSize(15)
        computer_label.setFont(computer_label_font)
        computer_column.addWidget(computer_label)

        algorithm_label = QLabel('Choose algorithm:')
        algorithm_label.setStyleSheet('font-size: 16px;color: #FFFFFF')
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(['group1', 'group2'])
        self.algorithm_combo.setStyleSheet('color: black')
        self.algorithm_combo.setFixedSize(500, 40)

        computer_column.addWidget(algorithm_label)
        computer_column.addWidget(self.algorithm_combo)

        # difficulty_label = QLabel('Choose difficulty level:')
        # difficulty_label.setStyleSheet('font-size: 16px;color: #FFFFFF')
        # self.difficulty_combo = QComboBox()
        # self.difficulty_combo.addItems(['1', '2', '3'])
        # self.difficulty_combo.setStyleSheet('color: black')
        # self.difficulty_combo.setFixedSize(500, 40)
        # computer_column.addWidget(difficulty_label)
        # computer_column.addWidget(self.difficulty_combo)

        player_row2.addLayout(computer_column)

        agent_column = QVBoxLayout()
        agent_label = QLabel('                          Grey Bot')
        agent_label_font = agent_label.font()
        agent_label_font.setBold(True)
        agent_label_font.setPointSize(15)
        agent_label.setFont(agent_label_font)
        agent_label.setStyleSheet('color: #FFFFFF')
        agent_column.addWidget(agent_label)

        algorithm_label1 = QLabel('Choose algorithm:')
        algorithm_label1.setStyleSheet('font-size: 16px;color: #FFFFFF')

        self.algorithm_combo1 = QComboBox()
        self.algorithm_combo1.addItems(['group1', 'group2'])
        self.algorithm_combo1.setStyleSheet('color: black')

        self.algorithm_combo1.setFixedSize(500, 40)
        agent_column.addWidget(algorithm_label1)
        agent_column.addWidget(self.algorithm_combo1)

        # difficulty_label1 = QLabel('Choose difficulty level:')
        # difficulty_label1.setStyleSheet('font-size: 16px;color: #FFFFFF')

        # self.difficulty_combo1 = QComboBox()
        # self.difficulty_combo1.addItems(['1', '2', '3'])
        # self.difficulty_combo1.setStyleSheet('color: black')
        # self.difficulty_combo1.setFixedSize(500, 40)

        # agent_column.addWidget(difficulty_label1)
        # agent_column.addWidget(self.difficulty_combo1)

        player_row2.addLayout(agent_column)
        main_layout.addLayout(player_row2)

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
        submit_button.clicked.connect(self.submit_clicked)

        main_layout.addWidget(submit_button)

        self.setLayout(main_layout)

    def submit_clicked(self):
        method1 = self.algorithm_combo.currentText()
        method2 = self.algorithm_combo1.currentText()
        self.close()
        print(method1)
        print(method2)
        play_game(method1, method2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CheckersWindow()
    window.show()
    sys.exit(app.exec_())