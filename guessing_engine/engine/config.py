# config.py: stores configuration values for the game.

import json
from pathlib import Path

defaults = {
    "use_rich": False,
    "bot_mode": False,
    "simulation": False,
    "leaderboard_sort": "insertion",
    "history_path": "data/history.json",
    "log_path": "data/game.log",
    "attempt_limit": None,
}

def hasRightType(name, value):
    
    """Check if the value is of the right type for the given setting name"""
    
    if name in ("use_rich", "bot_mode", "simulation"):
        return isinstance(value, bool)
    
    if name in ("leaderboard_sort", "history_path", "log_path"):
        return isinstance(value, str)
    
    if name == "attempt_limit":
        if value is None:
            return True
        return isinstance(value, int) and not isinstance(value, bool) and value >= 1
    
    return False

    
def loadConfig(path):
    
    """Load the configuration from a JSON file returning the settings and any problems"""
    
    settings = dict(defaults)
    problems = [] 

    if not Path(path).is_file():
        problems.append("config file missing so defaults used")
        return settings, problems

    try:
        with open(path, "r", encoding = "utf-8") as file:
            data = json.load(file)
    except (OSError, ValueError):
        data = None

    if not isinstance(data, dict):
        problems.append("config file broken so defaults used")
        return settings, problems

    for name in defaults:
        if name in data:
            if hasRightType(name, data[name]):
                settings[name] = data[name]
            else:
                problems.append("wrong type for " + name)

    return settings, problems