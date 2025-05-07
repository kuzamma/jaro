import json
import re
import os

class TextNormalizer:
    def __init__(self, leet_file='data/leet.json'):
        # Load leet mappings from file
        with open(leet_file, 'r') as f:
            self.leet_mapping = json.load(f)
    
    def normalize(self, text):
        """
        Convert leet speak to normal text and standardize input
        Args:
            text (str): Input text to normalize
        Returns:
            str: Normalized text
        """
        if not text:
            return text
            
        # Convert to lowercase
        text = text.lower()
        
        # Replace leet characters
        for char, replacement in self.leet_mapping.items():
            text = text.replace(char, replacement)
        
        # Remove repeated characters (e.g., "shittt" -> "shit")
        text = re.sub(r'(.)\1+', r'\1', text)
        
        return text