# Files Summary for Hugging Face Spaces Deployment

## Required Files for Deployment

### 1. `app.py` (Main Application)
- Gradio interface for the tokenizer
- Handles encoding, decoding, and round-trip testing
- Loads pre-trained tokenizer or trains if not found
- **Status**: ✅ Ready

### 2. `tokenizer.py` (Tokenizer Class)
- Core BPE tokenizer implementation
- Save/load functionality
- Encoding and decoding methods
- **Status**: ✅ Ready

### 3. `requirements.txt` (Dependencies)
- Contains: `gradio>=4.0.0`
- **Status**: ✅ Ready

### 4. `README.md` (Space Description)
- Description for Hugging Face Spaces
- Usage instructions
- Technical details
- **Status**: ✅ Ready

### 5. `Sanskrit.txt` (Training Data)
- Sanskrit text corpus for training
- **Status**: ✅ Present (required)

### 6. `sanskrit_tokenizer.pkl` (Pre-trained Tokenizer)
- Pre-trained tokenizer model
- **Status**: ⚠️ Not present (will be created on first run or by running `train_tokenizer.py`)

## Optional Files

### 7. `train_tokenizer.py` (Training Script)
- Script to pre-train the tokenizer
- Creates `sanskrit_tokenizer.pkl`
- **Status**: ✅ Ready (optional)

### 8. `DEPLOYMENT.md` (Deployment Guide)
- Step-by-step deployment instructions
- Troubleshooting guide
- **Status**: ✅ Ready

### 9. `.gitignore` (Git Ignore)
- Excludes unnecessary files from git
- **Status**: ✅ Ready

## Deployment Steps

1. **Pre-train tokenizer (recommended)**:
   ```bash
   python train_tokenizer.py
   ```
   This creates `sanskrit_tokenizer.pkl` to avoid retraining on Hugging Face Spaces.

2. **Clone Hugging Face Space**:
   ```bash
   git clone https://huggingface.co/spaces/AmolDuse/tokenizer-sanskrit
   cd tokenizer-sanskrit
   ```

3. **Copy files**:
   - Copy all the files listed above to the cloned repository

4. **Commit and push**:
   ```bash
   git add .
   git commit -m "Add Sanskrit BPE Tokenizer"
   git push
   ```

5. **Wait for build**:
   - Hugging Face Spaces will automatically build and deploy
   - Check the Space page for status

## Notes

- If `sanskrit_tokenizer.pkl` is not present, the app will train the tokenizer on first run (takes a few minutes)
- The tokenizer uses 5000 vocabulary tokens
- Training data (`Sanskrit.txt`) must be included in the repository
- The app will work without the pre-trained tokenizer, but startup will be slower

## Testing Locally

Before deploying, test locally:
```bash
pip install gradio
python app.py
```

Then open http://127.0.0.1:7860 in your browser.

