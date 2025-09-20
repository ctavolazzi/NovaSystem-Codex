import logging
import re
import uuid
import random
from abc import ABC, abstractmethod
import unittest

def generate_random_name(language='English', uuid_length=4, separator='-'):
    configurations = {
        'English': {
            'vowels': 'aeiou',
            'consonants': 'bcdfghjklmnpqrstvwxyz',
            'syllable_patterns': ['CVC', 'CV', 'VC', 'CVCV', 'VCV'],
            'weights': {
                'vowels': {v: 10 for v in 'aeiou'},
                'consonants': {c: 2 + (c in 'tnrsl') for c in 'bcdfghjklmnpqrstvwxyz'}
            }
        }
    }
    config = configurations.get(language, configurations['English'])
    vowels = ''.join([v * config['weights']['vowels'][v] for v in config['vowels']])
    consonants = ''.join([c * config['weights']['consonants'][c] for c in config['consonants']])
    pattern = random.choice(config['syllable_patterns'])
    name = []
    for char in pattern:
        if char == 'C':
            name.append(random.choice(consonants))
        elif char == 'V':
            name.append(random.choice(vowels))
    final_name = ''.join(name).capitalize()
    uuid_suffix = str(uuid.uuid4())[:uuid_length]
    if is_acceptable_name(final_name):
        return f"{final_name}{separator}{uuid_suffix}"
    else:
        return generate_random_name(language, uuid_length, separator)

def is_acceptable_name(name):
    unacceptable_sequences = ['xx', 'qq', 'uu', 'xyz', 'vwx']
    for seq in unacceptable_sequences:
        if seq in name:
            return False
    return True
#################    
### BOT START ###
#################    S
class Bot(ABC):
    def __init__(self, config):
        if 'name' not in config:
            self.name = generate_random_name()
        else:
            self.name = config['name']
        self.model = config.get('model', 'default_model')
        self.log_level = config.get('log_level', 'INFO')
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(getattr(logging, self.log_level.upper(), logging.INFO))
        self.log("Bot initialized with configuration.")

    def log(self, message, level=None):
        level_name = (level or self.log_level).upper()
        level_value = getattr(logging, level_name, logging.INFO)
        self.logger.log(level_value, message)

    @abstractmethod
    def execute(self, input_text):
        pass

    def say_name(self):
        return f"My name is {self.name}."

    def generate_random_phrase(self):
        phrases = [
            "I'm here to assist you!",
            "How can I help you today?",
            "I'm ready to answer your questions."
        ]
        return random.choice(phrases)
###############
### BOT END ###
###############
class CustomBot(Bot):
    def execute(self, input_text=None):
        self.log("Executing custom bot functionality.", level='INFO')

### TESTING ###
class TestBotInitialization(unittest.TestCase):
    def test_custom_bot_initialization(self):
        """Tests that CustomBot initializes correctly with a specific name."""
        bot = CustomBot({'name': 'TestBot', 'model': 'default_model', 'log_level': 'INFO'})
        self.assertEqual(bot.name, 'TestBot')
        self.assertEqual(bot.model, 'default_model')
        self.assertEqual(bot.log_level, 'INFO')

    def test_random_name_initialization(self):
        """Tests that CustomBot initializes with a generated name when no name is provided."""
        bot = CustomBot({'model': 'default_model', 'log_level': 'INFO'})
        self.assertRegex(
            bot.name,
            r'^[A-Z][a-z]+-[0-9a-f]{4}$'
        )  # Ensures a generated name with UUID suffix is used

    def test_logging(self):
        """Tests that CustomBot logs correctly at the DEBUG level."""
        bot = CustomBot({'name': 'LogTestBot', 'log_level': 'DEBUG'})
        with self.assertLogs(level='DEBUG') as log_context:
            bot.log("Testing debug level logging")
        self.assertIn('Testing debug level logging', log_context.output[0])

    def test_execute(self):
        """Tests the execute method for proper functionality."""
        bot = CustomBot({'name': 'ExecuteTestBot', 'log_level': 'INFO'})
        with self.assertLogs(level='INFO') as log_context:
            bot.execute()
        self.assertIn('Executing custom bot functionality.', log_context.output[0])

# Example usage
if __name__ == '__main__':
    unittest.main()