# Checkers AI Project

This project implements a Checkers game where two AI models play against each other using different algorithms. The game is built using **PyGame** for the game logic and **PyQt5** for the graphical user interface.

## Features
- Two AI players ("Purple Bot" and "Grey Bot") compete against each other.
- Supports selection of different algorithms for each AI player.
- Visual representation of the game with a custom-designed GUI.
- Performance metrics such as game execution time.

## Requirements
Ensure you have Python installed (preferably version 3.7 or above). Install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

### Dependencies
- PyQt5
- PyGame

## How to Run
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/Checkers-AI.git
   cd Checkers-AI
   ```
2. Run the main application:
   ```bash
   python main.py
   ```
3. Use the GUI to select algorithms for both bots and click "Play" to start the game.

## Project Structure
```
Checkers-AI/
├── main.py               # Main entry point for the application
├── group1.py             # Bot1
├── group2.py             # Bot2
├── components/           # Core logic for the game and AI bots
│   ├── GuiHandler.py     # Handles the game GUI
│   ├── AlgoBot.py        # AI bot logic and algorithms
├── resources/            # Visual assets
│   ├── background.jpg    # Background image for the GUI
│   ├── purpleBot.png     # Image for the Purple Bot
│   ├── greyBot.png       # Image for the Grey Bot
├── requirements.txt      # List of project dependencies
```

## Game Instructions
1. Upon launching the application, the GUI displays two bot players.
2. Select the desired algorithm for each bot (from the dropdown menus).
3. Click "Play" to start the game.
4. Watch as the two bots compete against each other in real time.

## Customization
- You can modify the AI algorithms in the `AlgoBot.py` file under the `components/` directory.
- Adjust the GUI design by editing `GuiHandler.py`.

## Known Issues
- Some performance lag may occur on older systems due to rendering.
- AI logic currently supports only the predefined algorithms ("group1" and "group2").

## Contributing
Contributions are welcome! If you'd like to improve the project, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- PyQt5 and PyGame libraries for enabling this project.
- Inspiration from classic board games and AI implementations.

---
