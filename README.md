# Number Guessing Engine

**Joshua Sullivan**  
CLASS-1a: Introduction to Studying Computer Science & AI and Robotics  
Design and Implement an Interactive Application

## Project Overview

The Number Guessing Engine is a Python terminal game developed for the CLASS-1a interactive application brief. The computer chooses a random whole number from 1 to 100. The player enters guesses and receives a higher or lower hint until the number is guessed. Invalid input is reported clearly without crashing the game or using a turn.

The project demonstrates input validation, control flow, classes, data structures and two manually implemented sorting algorithms. Player scores are kept for the current session and saved to an all-time history file. The session leaderboard is displayed in ascending order of turns before exit. Bot play and simulation modes are included as optional extras.

## Development Status

The application is now complete and runnable. All seven modules in `engine/` and the `main.py` entry point are implemented and the test suite passes (68 tests).

## Features

- **Play a game:** guess the secret number from 1 to 100 with too high or too low hints. Enter 1 to 3 letters as initials to save the score
- **Session leaderboard:** results from the current run ranked by fewest turns and shown again on exit
- **All-time leaderboard:** results saved between runs in `data/history.json`
- **Watch a bot game:** a binary search bot plays one game while the turn count is reported
- **Run bot simulation:** 1,000,000 games each for the binary bot and a random guessing bot using a fixed seed so results can be repeated. Fewest, most and average guesses are shown
- **Compare sort algorithms:** times insertion sort against merge sort on leaderboard sizes from 10 to 10,000 records (5 repeats per size)

## Design

- **Game and display separation:** `game.py` holds the secret number and win checks. `display.py` handles prompts and printed output only.
- **Input validation:** `validator.py` checks raw input as a whole number from 1 to 100 inclusive. Empty input, decimals, negatives, text and over-length input each give a specific error message and do not use a turn.
- **Manual sorting:** `sorting.py` contains an insertion sorter and a merge sorter built on a shared `Sorter` base class. Python's built-in sorting functions are not used anywhere in the engine. The leaderboard sort is chosen in the config file.
- **Leaderboard:** records hold initials, turns, timestamp and source. Only human player records are accepted so bot scores can never enter a leaderboard.
- **Saved history:** `storage.py` loads and saves human results separately from the event log. A missing or empty history file is treated as no history. A broken file or invalid entries are skipped and logged so startup is never blocked. Saves write to a temporary file first and then replace the original to avoid corrupting existing data.
- **Optional Rich styling:** `use_rich` switches to a styled display when Rich is installed. The basic display is the default and works with no extra packages.
- **Configuration:** `config.json` is checked on load. A missing file or a wrong type falls back to a safe default and is logged. The secret range is fixed at 1 to 100 and `attempt_limit` is `null` by default so the game continues until the correct guess.

## Configuration

Settings are in `guessing_engine/config.json`.

| Setting | Default in code | Shipped config | Purpose |
| --- | --- | --- | --- |
| `use_rich` | `false` | `false` | Use the Rich display instead of the basic one |
| `bot_mode` | `false` | `true` | Show the Watch a Bot Game menu option |
| `simulation_mode` | `false` | `true` | Show the simulation and sort comparison options |
| `leaderboard_sort` | `"insertion"` | `"insertion"` | Sorting algorithm used for the leaderboard (`"insertion"` or `"merge"`) |
| `history_storage` | `"data/history.json"` | same | Where all-time results are saved |
| `log_storage` | `"data/game.log"` | same | Where the event log is written |
| `attempt_limit` | `null` | `null` | Maximum guesses per game (`null` means unlimited) |

## Project Layout

```text
01_Interactive_Application/
|-- .gitignore
|-- README.md
`-- guessing_engine/
    |-- main.py
    |-- config.json
    |-- pyproject.toml
    |-- engine/
    |   |-- __init__.py
    |   |-- bot.py
    |   |-- config.py
    |   |-- display.py
    |   |-- game.py
    |   |-- leaderboard.py
    |   |-- simulation.py
    |   |-- sorting.py
    |   |-- storage.py
    |   `-- validator.py
    |-- data/            (created automatically when the game first saves)
    `-- tests/
        |-- test_bot.py
        |-- test_config.py
        |-- test_game.py
        |-- test_leaderboard.py
        |-- test_sorting.py
        |-- test_storage.py
        `-- test_validator.py
```

`main.py` is the entry point and manages the menu loop. Each `engine/` module has one job as described in the Design section. Tests are grouped by the module they cover. Runtime history and log files are written to `data/`.

## Install

Python 3.10 or newer is needed. The game itself has no required packages. Optional extras are installed with:

```bash
pip install rich pytest
```

Rich is only needed if `use_rich` is set to `true`. Pytest is only needed to run the tests.

## Run

From the `guessing_engine` folder:

```bash
python main.py
```

The menu offers seven options. Type the number of the option you want. Options 4 to 6 only work when `bot_mode` and `simulation_mode` are enabled in the config file.

1. Play a Game
2. Session Leaderboard
3. All-Time Leaderboard
4. Watch a Bot Game
5. Run Bot Simulation
6. Compare Sort Algorithms
7. Exit Program

## Tests

From the `guessing_engine` folder:

```bash
python -m pytest
```

The tests cover validator edge cases, both sorting algorithms (empty, single item, sorted, reversed and duplicate inputs), leaderboard handling, bot guess limits, storage failures and configuration defaults.

## Experiments

Option 5 compares the binary search bot against random guessing over 1,000,000 seeded games. A binary search bot should never need more than 7 guesses for a range of 100 so the results can be checked against that expectation. Option 6 times insertion sort against merge sort as the leaderboard grows. The method, data, limitations and charts for both experiments are in the supporting documentation.

## Assignment Submission

The brief requests a working Python application in the `01_Interactive_Application` submission folder packaged with all required files. Supporting documentation should include application screenshots, explained code snippets, design or pseudocode, development reflection and references. A separate reflective learning summary is also required. This repository covers the interactive application portion. The submission deadline is 4 December 2026.
