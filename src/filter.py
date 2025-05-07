from .similarity import jaro_similarity
from .normalizer import TextNormalizer
import json
import re

class BadWordFilter:
    def __init__(self, bad_words_file, euphemisms_file, threshold=0.85):
        with open(bad_words_file, 'r') as f:
            self.bad_words = [line.strip().lower() for line in f if line.strip()]
        
        with open(euphemisms_file, 'r') as f:
            self.euphemisms = json.load(f)
        
        self.threshold = threshold
        self.normalizer = TextNormalizer()
        self.word_pattern = re.compile(r"(\w+|\W)")  # Improved pattern
    
    def normalize_input(self, text):
        return self.normalizer.normalize(text)
    
    def find_closest_match(self, word):
        normalized_word = self.normalize_input(word)
        max_sim = 0
        best_match = None
        
        for bad_word in self.bad_words:
            # Compare normalized versions
            sim = jaro_similarity(normalized_word, self.normalize_input(bad_word))
            if sim > max_sim and sim >= self.threshold:
                max_sim = sim
                best_match = bad_word
        
        return (best_match, max_sim) if best_match else (None, 0)
    
    def get_replacement(self, bad_word):
        return self.euphemisms.get(bad_word.lower(), bad_word)
    
    def filter_text(self, text):
        # Split into tokens while preserving original structure
        tokens = self.word_pattern.finditer(text)
        filtered_text = []
        
        for match in tokens:
            token = match.group()
            
            # Only process word tokens
            if token.isalpha():
                # Find matches using normalized version
                match_result, _ = self.find_closest_match(token)
                if match_result:
                    replacement = self.get_replacement(match_result)
                    # Preserve original capitalization
                    if token[0].isupper():
                        replacement = replacement.capitalize()
                    filtered_text.append(replacement)
                else:
                    filtered_text.append(token)
            else:
                # Handle leet-speak within words (like "cr@p")
                if any(char in self.normalizer.leet_mapping for char in token.lower()):
                    # Normalize just this token for checking
                    normalized_token = self.normalize_input(token)
                    match_result, _ = self.find_closest_match(normalized_token)
                    if match_result:
                        replacement = self.get_replacement(match_result)
                        # Preserve original capitalization
                        if token[0].isupper():
                            replacement = replacement.capitalize()
                        filtered_text.append(replacement)
                    else:
                        filtered_text.append(token)
                else:
                    filtered_text.append(token)
        
        return ''.join(filtered_text)