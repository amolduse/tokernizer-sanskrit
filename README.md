---
title: Sanskrit BPE Tokenizer
emoji: 🕉️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# 🕉️ Sanskrit BPE Tokenizer

A Byte Pair Encoding (BPE) tokenizer trained on Sanskrit text with a vocabulary of 5000+ tokens.

## Features

- **Encode Sanskrit text** into token IDs
- **Decode token IDs** back to Sanskrit text
- **Round-trip encoding/decoding** with verification
- **5000+ token vocabulary** trained on Sanskrit corpus
- **~30X compression ratio**

## How to Use

1. **Encode Text**: Enter Sanskrit text in Devanagari script and get token IDs
2. **Decode Tokens**: Enter token IDs (as a list) to get back the Sanskrit text
3. **Encode & Decode**: Test round-trip encoding to verify tokenization quality

## Tokenizer Details

- **Vocabulary Size**: 5000 tokens
- **Base Tokens**: 256 (UTF-8 bytes)
- **Learned Merges**: 4744
- **Compression Ratio**: ~30X
- **Training Data**: Sanskrit.txt corpus

## Technical Details

This tokenizer uses Byte Pair Encoding (BPE) algorithm optimized for Sanskrit text. It:
- Starts with UTF-8 byte encoding
- Iteratively merges most frequent byte pairs
- Builds a vocabulary of 5000 tokens
- Handles Unicode encoding automatically

## Examples

- Input: `एकवचनम्`
- Output: `[256, 370, 401, 273, 258]`

## License

MIT License

## Author

AmolDuse

