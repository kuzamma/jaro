from src.filter import BadWordFilter
from config import BAD_WORDS_FILE, EUPHEMISMS_FILE, SIMILARITY_THRESHOLD

def main():
    # Initialize the filter
    word_filter = BadWordFilter(
        bad_words_file=BAD_WORDS_FILE,
        euphemisms_file=EUPHEMISMS_FILE,
        threshold=SIMILARITY_THRESHOLD
    )
    
    # Example usage
    test_texts = [
        "What the fuck is going on here?",
        "This is some bullshit!",
        "Don't be such an asshole.",
        "Oh damn, that's unfortunate.",
        "I stepped in some sh!t cr@p.",
        "That's a shit take mushroom, not a bad word!"
    ]
    
    for text in test_texts:
        filtered = word_filter.filter_text(text)
        print(f"Original: {text}")
        print(f"Filtered: {filtered}")
        print("-" * 50)

if __name__ == "__main__":
    main()