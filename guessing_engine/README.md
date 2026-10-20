# Number Guessing Engine

**Joshua Sullivan**  
CLASS-1a: Introduction to Studying Computer Science & AI and Robotics  
Design and Implement an Interactive Application

## Project Overview

The Number Guessing Engine is a Python terminal game developed for the CLASS-1a interactive application brief. In the core game the computer chooses a random whole number from 1 to 100. The player enters guesses and receives a higher or lower hint until the number is guessed. Invalid input should be reported clearly without crashing the game or using a turn.

The project is designed to demonstrate input validation, control flow, classes, data structures and a manually implemented sorting algorithm. Human scores are kept for the current session and displayed in ascending order before exit. The design also plans for saved score history and optional bot and simulation modes.

## Development Status

This repository currently contains the project scaffold. The Python modules and entry point are placeholders, so the game is not yet runnable. This README describes the target behavior and planned structure. I need to update the run instructions as the implementation is completed.

## Design

- **Game and display separation:** Game state and win checks belong in the game logic, display code handles prompts and printed output.
- **Input validation:** Raw terminal input is checked as a whole number in the inclusive range 1-100. Empty input, decimals, symbols and out-of-range values should produce useful errors and leave the valid-turn count unchanged.
- **Session leaderboard:** Record human player initials and valid turns in memory. Before exiting use a sorting algorithm to show the lowest turn counts first. Do not use Python's built-in sorting functions for anything.
- **Two sorting algorithms:** Implement two interchangeable manual sorts and compare their performance as a planned experiment.
- **Saved history:** Load and save human results separately from the event log. A missing, empty or broken history file should not prevent startup. An all-time history view is planned in addition to the required session leaderboard.
- **Optional features:** Bot play, simulations and Rich terminal styling are secondary to the core game and tests. Bot scores must not enter the human leaderboard. Rich must remain optional and have a plain-text fallback.
- **Configuration:** Keep the secret range fixed at 1-100. Settings should have safe defaults and any attempt limit should be disabled by default so the game continues until the correct guess.

## Project Layout

```text
guessing_engine/
|-- main.py
|-- config.json
|-- pyproject.toml
|-- README.md
|-- engine/
|   |-- bot.py
|   |-- config.py
|   |-- display.py
|   |-- game.py
|   |-- leaderboard.py
|   |-- simulation.py
|   |-- sorting.py
|   |-- start.py
|   |-- storage.py
|   `-- validator.py
|-- data/
`-- tests/
	|-- test_bot.py
	|-- test_leaderboard.py
	|-- test_sorting.py
	|-- test_storage.py
	`-- test_validator.py
```

`main.py` is intended to be the entry point. The `engine/` modules follow the responsibilities above. Tests are grouped by the module they cover. Runtime history and log files will be stored in `data/` when storage is implemented.

## Setup and Commands

Python 3.10 or newer is required. The core game is intended to use only the Python standard library. Install the optional test or Rich dependencies from the project directory when needed:

```powershell
python -m pip install -e ".[test]"
python -m pip install -e ".[rich]"
```

When the entry point and game are implemented, start the application from this directory with:

```powershell
python main.py
```

Run the test suite with:

```powershell
python -m pytest
```

## Planned Tests and Experiments

Tests will cover validator edge cases; both sorting algorithms on empty, single-item, sorted, reversed and duplicate inputs; leaderboard tie handling; bot guess limits; storage failures and configuration defaults. The planned experiments compare sort timings as leaderboard size grows. Measure bot guess counts against binary-search expectations and compare bot play with random guessing in simulation. Results should include the method, data, limitations and a chart in the supporting documentation.

## Assignment Submission

The brief requests a working Python application in the `01_Interactive_Application` submission folder packaged with all required files. Supporting documentation should include application screenshots, explained code snippets, design or pseudocode, development reflection and references. A separate reflective learning summary is also required. This repository covers the interactive application portion.
