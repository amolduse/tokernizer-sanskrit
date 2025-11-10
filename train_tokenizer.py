# -*- coding: utf-8 -*-
"""
Script to train and save the Sanskrit BPE tokenizer.
Run this before deploying to Hugging Face Spaces to save training time.
"""

import os
from tokenizer import SanskritBPETokenizer

def main():
    """Train and save the tokenizer."""
    if not os.path.exists('Sanskrit.txt'):
        print("Error: Sanskrit.txt file not found!")
        return
    
    print("Loading Sanskrit text...")
    with open('Sanskrit.txt', 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    
    print(f"Text length: {len(text)} characters")
    print("Training tokenizer (this may take a few minutes)...")
    
    tokenizer = SanskritBPETokenizer(vocab_size=5000, verbose=True)
    tokenizer.train(text)
    
    print(f"\nSaving tokenizer to sanskrit_tokenizer.pkl...")
    tokenizer.save('sanskrit_tokenizer.pkl')
    
    print(f"Tokenizer saved!")
    print(f"Vocabulary size: {len(tokenizer.vocab)}")
    print(f"Number of merges: {len(tokenizer.merges)}")
    
    # Test encoding/decoding
    test_text = "एकवचनम्"
    encoded = tokenizer.encode(test_text)
    decoded = tokenizer.decode(encoded)
    
    print(f"\nTest:")
    print(f"Original: {test_text}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
    print(f"Match: {test_text == decoded}")

if __name__ == "__main__":
    main()

