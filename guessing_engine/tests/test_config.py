# test_config.py: tests the configuration values for the game

import json # import the json module to handle JSON data
from pathlib import Path # import the Path class from the pathlib module to handle file paths
from engine.config import loadConfig, hasRightType, defaults # import the loadConfig and hasRightType functions and the defaults dictionary from the engine.config module

def writeConfig(folder, text): # A function that writes a given text to a config.json file in a specified folder and returns the path to the file as a string.
    
    """Write the given text to a config.json file in the specified folder and return the path to the file as a string."""
    
    path = folder / "config.json" # Create a Path object for the config.json file in the specified folder
    path.write_text(text, encoding = "utf-8") # Write the given text to the config.json file using UTF-8 encoding
    return str(path) # Return the path to the config.json file as a string


class TestConfig: # A class that contains tests for the loadConfig and hasRightType functions. The tmp_path argument is a fresh empty folder that pytest makes for each test and removes afterwards
    
    """A class that holds tests for the loadConfig and hasRightType functions. The tmp_path argument is a fresh empty folder that pytest makes for each test and removes afterwards."""
    
    def testMissingFileGivesDefaults(self, tmp_path): # A test that checks if a missing config file returns the default settings and reports a problem
        
        """Test that a missing config file gives the defaults and one problem."""
        
        settings, problems = loadConfig(str(tmp_path / "nothing.json")) # Load the configuration from a non-existent file and capture the returned settings and problems
        assert settings == defaults, "The defaults should be used." # Assert that the returned settings are equal to the default settings indicating that the defaults were used due to the missing file
        assert problems == ["config file missing so defaults used"], "The problem should say the file is missing." # Assert that the returned problems list contains a message indicating that the config file was missing and defaults were used confirming that the appropriate problem was reported

    def testBrokenJsonGivesDefaults(self, tmp_path): # A test that checks if a broken JSON config file returns the default settings and reports a problem
        
        """Test that a broken JSON config file gives the defaults and one problem."""
        
        path = writeConfig(tmp_path, "{ this is not json") # Write a broken JSON string to a config.json file in the temporary folder and get the path to the file
        settings, problems = loadConfig(path) # Load the configuration from the broken JSON file and capture the returned settings and problems
        assert settings == defaults, "The defaults should be used." # Assert that the returned settings are equal to the default settings indicating that the defaults were used due to the broken JSON file
        assert problems == ["config file broken so defaults used"], "The problem should say the file is broken." # Assert that the returned problems list contains a message indicating that the config file was broken and defaults were used confirming that the appropriate problem was reported

    def testEmptyFileGivesDefaults(self, tmp_path): # A test that checks if an empty config file returns the default settings and reports a problem
        
        """Test that an empty config file gives the defaults and at least one problem."""
        
        path = writeConfig(tmp_path, "") # Write an empty string to a config.json file in the temporary folder and get the path to the file
        settings, problems = loadConfig(path) # Load the configuration from the empty file and capture the returned settings and problems
        assert settings == defaults, "The defaults should be used." # Assert that the returned settings are equal to the default settings indicating that the defaults were used due to the empty config file
        assert len(problems) >= 1, "There should be a problem." # Assert that the length of the returned problems list is at least 1 indicating that there was at least one problem reported due to the empty config file

    def testNotADictionaryGivesDefaults(self, tmp_path): # A test that checks if a config file containing valid JSON that is not a dictionary returns the default settings and reports a problem
        
        """Test that a config file containing valid JSON that is not a dictionary gives the defaults and one problem."""
        
        path = writeConfig(tmp_path, "[1, 2, 3]") # Write a valid JSON array to a config.json file in the temporary folder and get the path to the file
        settings, problems = loadConfig(path) # Load the configuration from the file containing valid JSON that is not a dictionary and capture the returned settings and problems
        assert settings == defaults, "The defaults should be used." # Assert that the returned settings are equal to the default settings indicating that the defaults were used due to the config file not being a dictionary
        assert problems == ["config file broken so defaults used"], "The problem should say the file is broken." # Assert that the returned problems list contains a message indicating that the config file was broken and defaults were used confirming that the appropriate problem was reported

    def testGoodValuesOverrideTheDefaults(self, tmp_path): # A test that checks if a config file containing valid settings overrides the default settings with no problems
        
        """Test that a config file containing valid settings overrides the default settings with no problems."""
        
        path = writeConfig(tmp_path, json.dumps({"use_rich": True, "leaderboard_sort": "merge", "attempt_limit": 10})) # Write a valid JSON object with specific settings to a config.json file in the temporary folder and get the path to the file
        settings, problems = loadConfig(path) # Load the configuration from the file containing valid settings and capture the returned settings and problems
        assert settings["use_rich"] == True, "use_rich should be changed." # Assert that the "use_rich" setting in the returned settings is True indicating that it was successfully overridden from the default value
        assert settings["leaderboard_sort"] == "merge", "leaderboard_sort should be changed." # Assert that the "leaderboard_sort" setting in the returned settings is "merge" indicating that it was successfully overridden from the default value
        assert settings["attempt_limit"] == 10, "attempt_limit should be changed." # Assert that the "attempt_limit" setting in the returned settings is 10 indicating that it was successfully overridden from the default value
        assert settings["bot_mode"] == False, "Settings that were not in the file keep their default." # Assert that the "bot_mode" setting in the returned settings is still False indicating that it retained its default value since it was not specified in the config file
        assert problems == [], "There should be no problems." # Assert that the returned problems list is empty indicating that there were no problems reported when loading the valid settings from the config file

    def testWrongTypeKeepsTheDefault(self, tmp_path): # A test that checks if a config file containing a setting with the wrong type keeps its default value and reports a problem while other valid settings still load correctly.
        
        """Test that a config file containing a setting with the wrong type keeps its default value and reports a problem while other valid settings still load correctly."""
        
        path = writeConfig(tmp_path, json.dumps({"use_rich": "yes", "bot_mode": True})) # Write a valid JSON object with a setting that has the wrong type and another valid setting to a config.json file in the temporary folder and get the path to the file
        settings, problems = loadConfig(path) # Load the configuration from the file containing a setting with the wrong type and another valid setting and capture the returned settings and problems
        assert settings["use_rich"] == False, "The bad value should keep its default." # Assert that the "use_rich" setting in the returned settings is still False indicating that it was retained its default value due to the wrong type specified in the config file
        assert settings["bot_mode"] == True, "The good value should still load." # Assert that the "bot_mode" setting in the returned settings is True indicating that it was successfully loaded from the config file since it had the correct type
        assert problems == ["wrong type for use_rich"], "The problem should name the setting."  # Assert that the returned problems list contains a message indicating that there was a wrong type for the "use_rich" setting, confirming that the appropriate problem was reported

    def testUnknownSettingsAreIgnored(self, tmp_path): # A test that checks if a config file containing an unknown setting ignores that setting and does not report any problems.
        
        """Test that a config file containing an unknown setting ignores that setting and does not report any problems."""
        
        path = writeConfig(tmp_path, json.dumps({"secret_range": 500})) # Write a valid JSON object with an unknown setting to a config.json file in the temporary folder and get the path to the file
        settings, problems = loadConfig(path) # Load the configuration from the file containing an unknown setting and capture the returned settings and problems
        assert "secret_range" not in settings, "Unknown settings should not be added." # Assert that the "secret_range" setting is not present in the returned settings indicating that unknown settings are ignored and not added to the configuration
        assert problems == [], "Unknown settings are not a problem." # Assert that the returned problems list is empty indicating that there were no problems reported when loading the config file with an unknown setting

    def testAttemptLimitRules(self): # A test that checks if the "attempt_limit" setting can be None or a whole number of 1 or more and nothing else.
        
        """Test that the "attempt_limit" setting can be None or a whole number of 1 or more and nothing else."""
        
        assert hasRightType("attempt_limit", None) == True, "None means unlimited so it is allowed." # Assert that the "attempt_limit" setting can be None indicating that it is allowed and means unlimited attempts
        assert hasRightType("attempt_limit", 5) == True, "A positive whole number is allowed." # Assert that the "attempt_limit" setting can be a positive whole number indicating that it is allowed and represents a valid limit on attempts
        assert hasRightType("attempt_limit", 1) == True, "1 is the smallest allowed limit." # Assert that the "attempt_limit" setting can be 1 indicating that it is allowed and represents the smallest valid limit on attempts
        assert hasRightType("attempt_limit", 0) == False, "0 is not allowed." # Assert that the "attempt_limit" setting cannot be 0 indicating that it is not allowed and does not represent a valid limit on attempts
        assert hasRightType("attempt_limit", -2) == False, "Negative numbers are not allowed." # Assert that the "attempt_limit" setting cannot be a negative number indicating that it is not allowed and does not represent a valid limit on attempts
        assert hasRightType("attempt_limit", 2.5) == False, "Decimals are not allowed." # Assert that the "attempt_limit" setting cannot be a decimal indicating that it is not allowed and does not represent a valid limit on attempts
        assert hasRightType("attempt_limit", True) == False, "True must not count as the number 1." # Assert that the "attempt_limit" setting cannot be True indicating that it is not allowed and does not represent a valid limit on attempts

    def testOtherTypeRules(self): # A test that checks if booleans must be real booleans paths must be text and unknown setting names are rejected.
        
        """Test that booleans must be real booleans paths must be text and unknown setting names are rejected."""
        
        assert hasRightType("use_rich", True) == True, "A boolean is allowed." # Assert that the "use_rich" setting can be a boolean value indicating that it is allowed and represents a valid configuration option
        assert hasRightType("use_rich", 1) == False, "A number is not a boolean." # Assert that the "use_rich" setting cannot be a number indicating that it is not allowed and does not represent a valid configuration option
        assert hasRightType("history_storage", "data/history.json") == True, "Text is allowed for a path." # Assert that the "history_storage" setting can be a string representing a file path indicating that it is allowed and represents a valid configuration option
        assert hasRightType("history_storage", 5) == False, "A number is not a path." # Assert that the "history_storage" setting cannot be a number indicating that it is not allowed and does not represent a valid configuration option
        assert hasRightType("not_a_setting", True) == False, "Unknown setting names are rejected." # Assert that the "not_a_setting" setting cannot be a boolean indicating that it is not allowed and does not represent a valid configuration option

    def testTheRealConfigFileIsValid(self): # A test that checks if the real config.json file in the project loads with no problems and has the expected default values.
        
        """Test that the real config.json file in the project loads with no problems and has the expected default values."""
        
        path = Path(__file__).parent.parent / "config.json" # Create a Path object for the real config.json file in the project directory
        settings, problems = loadConfig(str(path)) # Load the configuration from the real config.json file and capture the returned settings and problems
        assert problems == [], "The real config file should have no problems." # Assert that the returned problems list is empty indicating that there were no problems reported when loading the real config.json file
        assert settings["attempt_limit"] is None, "The attempt limit should be off by default." # Assert that the "attempt_limit" setting in the returned settings is None indicating that it is off by default as expected
