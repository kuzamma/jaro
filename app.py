from flask import Flask, render_template, request, jsonify
import json
import re
import os
import random
from datetime import datetime

app = Flask(__name__)

# Configuration paths
DATA_DIR = 'data'
BAD_WORDS_FILE = os.path.join(DATA_DIR, 'bad-words.txt')
EUPHEMISMS_FILE = os.path.join(DATA_DIR, 'euphemisms.json')
LEET_MAPPINGS_FILE = os.path.join(DATA_DIR, 'leet-mappings.json')

def load_leet_mappings():
    """Load leet speak mappings from JSON file with UTF-8 encoding"""
    default_mappings = {
        '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '0': 'o',
        '@': 'a', '!': 'i', '$': 's', '#': 'h', '+': 't', '©': 'c'
    }
    
    try:
        with open(LEET_MAPPINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {LEET_MAPPINGS_FILE} not found. Using default leet mappings.")
        return default_mappings
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Warning: Error loading {LEET_MAPPINGS_FILE}. Using defaults. Error: {e}")
        return default_mappings

def load_bad_words():
    """Load bad words with UTF-8 encoding"""
    try:
        with open(BAD_WORDS_FILE, 'r', encoding='utf-8') as f:
            return [word.strip().lower() for word in f if word.strip()]
    except FileNotFoundError:
        print(f"Error: {BAD_WORDS_FILE} not found. Using empty bad words list.")
        return []

def load_euphemisms():
    """Load euphemisms with UTF-8 encoding"""
    try:
        with open(EUPHEMISMS_FILE, 'r', encoding='utf-8') as f:
            euphemisms = json.load(f)
            # Convert single strings to lists for backward compatibility
            for k, v in euphemisms.items():
                if isinstance(v, str):
                    euphemisms[k] = [v]
            return euphemisms
    except FileNotFoundError:
        print(f"Error: {EUPHEMISMS_FILE} not found. Using empty replacements.")
        return {}
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Error: Invalid {EUPHEMISMS_FILE}. Using empty replacements. Error: {e}")
        return {}

# Load all data files with UTF-8 encoding
LEET_MAP = load_leet_mappings()
BAD_WORDS = load_bad_words()
REPLACEMENTS = load_euphemisms()

class TextNormalizer:
    def __init__(self, mappings):
        self.leet_mapping = mappings
    
    def normalize(self, text):
        """Convert leet speak to normal text"""
        if not text:
            return text
            
        text = text.lower()
        for char, replacement in self.leet_mapping.items():
            text = text.replace(char, replacement)
        return text

    def get_replacement(self, bad_word):
        """Get a random euphemism from available options"""
        options = REPLACEMENTS.get(bad_word.lower(), [bad_word])
        return random.choice(options)

# Initialize normalizer
normalizer = TextNormalizer(LEET_MAP)

def contains_bad_word(word):
    """Check if word contains any bad word (including leet versions)"""
    # Check original word
    if word.lower() in BAD_WORDS:
        return word.lower()
    
    # Check normalized version
    normalized = normalizer.normalize(word)
    if normalized in BAD_WORDS:
        return normalized
    
    # Check if word contains bad word with special characters
    for bad_word in BAD_WORDS:
        if bad_word in normalized:
            return bad_word
    
    return None

def filter_text(text):
    """Filter text by replacing bad words with random euphemisms"""
    tokens = re.findall(r"([a-zA-Z0-9@$!©]+|[\W_])", text)
    filtered_tokens = []
    
    for token in tokens:
        if not token.isalnum() and not any(c.isalnum() for c in token):
            filtered_tokens.append(token)
            continue
        
        bad_word = contains_bad_word(token)
        if bad_word:
            replacement = normalizer.get_replacement(bad_word)
            # Preserve original capitalization
            if token[0].isupper():
                replacement = replacement.capitalize()
            filtered_tokens.append(replacement)
        else:
            filtered_tokens.append(token)
    
    return ''.join(filtered_tokens)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/filter', methods=['POST'])
def filter_handler():
    text = request.form.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    filtered = filter_text(text)
    
    return jsonify({
        'original': text,
        'filtered': filtered,
        'normalized': normalizer.normalize(text),
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'status': 'success'
    })

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)