import os

# Get the directory where this config file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')
BAD_WORDS_FILE = os.path.join(DATA_DIR, 'bad-words.txt')
EUPHEMISMS_FILE = os.path.join(DATA_DIR, 'euphemisms.json')

# Jaro similarity threshold (0.0 to 1.0)
SIMILARITY_THRESHOLD = 0.85