# -*- coding: utf-8 -*-
"""
BPE (Byte Pair Encoding) Tokenizer for Sanskrit
A clean implementation of BPE tokenization optimized for Sanskrit text.
"""

import pickle
import os


class SanskritBPETokenizer:
    """BPE Tokenizer for Sanskrit text."""
    
    def __init__(self, vocab_size=5000, verbose=False):
        """
        Initialize the BPE tokenizer.
        
        Args:
            vocab_size: Target vocabulary size (default: 5000)
            verbose: Whether to print progress information (default: False)
        """
        self.vocab_size = vocab_size
        self.verbose = verbose
        self.merges = {}
        self.vocab = {}
        
    def get_stats(self, ids):
        """Get frequency statistics of byte pairs."""
        counts = {}
        for pair in zip(ids, ids[1:]):
            counts[pair] = counts.get(pair, 0) + 1
        return counts
    
    def merge(self, ids, pair, idx):
        """Merge a byte pair into a single token."""
        newids = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and ids[i] == pair[0] and ids[i+1] == pair[1]:
                newids.append(idx)
                i += 2
            else:
                newids.append(ids[i])
                i += 1
        return newids
    
    def train(self, text):
        """
        Train the BPE tokenizer on Sanskrit text.
        
        Args:
            text: Sanskrit text string to train on
        """
        # Convert text to bytes
        tokens = list(text.encode('utf-8'))
        
        # Initialize vocabulary with base 256 bytes
        num_merges = self.vocab_size - 256
        ids = list(tokens)
        self.merges = {}
        
        # Perform BPE merges
        for i in range(num_merges):
            stats = self.get_stats(ids)
            if not stats:
                break
                
            pair = max(stats, key=stats.get)
            idx = 256 + i
            
            if self.verbose and (i + 1) % 250 == 0:
                print(f"Progress: {i + 1}/{num_merges} merges completed")
            
            ids = self.merge(ids, pair, idx)
            self.merges[pair] = idx
        
        # Build vocabulary
        self.vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in self.merges.items():
            self.vocab[idx] = self.vocab[p0] + self.vocab[p1]
        
        if self.verbose:
            compression_ratio = len(tokens) / len(ids) if ids else 0
            print(f"Training complete: {len(self.merges)} merges, "
                  f"compression ratio: {compression_ratio:.2f}X")
    
    def encode(self, text):
        """
        Encode Sanskrit text into token IDs.
        
        Args:
            text: Sanskrit text string to encode
            
        Returns:
            List of token IDs
        """
        tokens = list(text.encode('utf-8'))
        
        while len(tokens) >= 2:
            stats = self.get_stats(tokens)
            if not stats:
                break
                
            # Find the pair with the lowest merge index
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            
            if pair not in self.merges:
                break  # nothing else can be merged
            
            idx = self.merges[pair]
            tokens = self.merge(tokens, pair, idx)
        
        return tokens
    
    def decode(self, ids):
        """
        Decode token IDs back to Sanskrit text.
        
        Args:
            ids: List of token IDs to decode
            
        Returns:
            Decoded Sanskrit text string
        """
        tokens = b"".join(self.vocab[idx] for idx in ids)
        text = tokens.decode('utf-8', errors="replace")
        return text
    
    def save(self, filepath):
        """Save tokenizer to file."""
        data = {
            'vocab_size': self.vocab_size,
            'merges': {f"{k[0]},{k[1]}": v for k, v in self.merges.items()},
            'vocab': {k: list(v) for k, v in self.vocab.items()}
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, filepath):
        """Load tokenizer from file."""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.vocab_size = data['vocab_size']
        # Convert merges back from string keys to tuples
        self.merges = {tuple(map(int, k.split(','))): v for k, v in data['merges'].items()}
        # Convert vocab back to bytes
        self.vocab = {k: bytes(v) for k, v in data['vocab'].items()}

