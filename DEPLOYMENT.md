# Deployment Guide for Hugging Face Spaces

This guide explains how to deploy the Sanskrit BPE Tokenizer to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account
2. Git installed on your machine
3. Access to the Hugging Face Space: https://huggingface.co/spaces/AmolDuse/tokenizer-sanskrit

## Step 1: Clone the Repository

```bash
git clone https://huggingface.co/spaces/AmolDuse/tokenizer-sanskrit
cd tokenizer-sanskrit
```

## Step 2: Prepare Files

Ensure you have the following files in your repository:

- `app.py` - Gradio application
- `tokenizer.py` - Tokenizer class
- `requirements.txt` - Python dependencies
- `README.md` - Space description
- `Sanskrit.txt` - Training data
- `sanskrit_tokenizer.pkl` - Pre-trained tokenizer (optional but recommended)

## Step 3: Pre-train the Tokenizer (Optional but Recommended)

To avoid retraining on every deployment, pre-train the tokenizer locally:

```bash
python train_tokenizer.py
```

This will create `sanskrit_tokenizer.pkl` which should be committed to the repository.

## Step 4: Commit and Push

```bash
git add .
git commit -m "Add Sanskrit BPE Tokenizer"
git push
```

## Step 5: Verify Deployment

1. Go to https://huggingface.co/spaces/AmolDuse/tokenizer-sanskrit
2. Wait for the Space to build (usually 2-5 minutes)
3. Test the tokenizer interface

## File Structure

```
tokenizer-sanskrit/
├── app.py                 # Gradio application
├── tokenizer.py           # Tokenizer class
├── requirements.txt       # Dependencies
├── README.md             # Space description
├── Sanskrit.txt          # Training data
├── sanskrit_tokenizer.pkl # Pre-trained tokenizer
├── train_tokenizer.py    # Training script (optional)
└── .gitignore           # Git ignore file
```

## Important Notes

1. **Pre-trained Tokenizer**: If `sanskrit_tokenizer.pkl` exists, the app will load it instead of retraining. This significantly reduces startup time.

2. **Training Data**: The `Sanskrit.txt` file must be included in the repository for the tokenizer to work.

3. **Dependencies**: Only `gradio` is required in `requirements.txt` as the tokenizer uses only standard library modules.

4. **Memory**: The tokenizer uses minimal memory. A CPU instance on Hugging Face Spaces should be sufficient.

## Troubleshooting

### Issue: Tokenizer takes too long to load
**Solution**: Pre-train the tokenizer locally and commit `sanskrit_tokenizer.pkl` to the repository.

### Issue: Sanskrit.txt not found
**Solution**: Ensure `Sanskrit.txt` is included in the repository and committed.

### Issue: Module not found errors
**Solution**: Check that `requirements.txt` includes all necessary dependencies (only `gradio` is needed).

## Testing Locally

Before deploying, test the app locally:

```bash
pip install gradio
python app.py
```

Then open the local URL shown in the terminal (usually http://127.0.0.1:7860).

## Updating the Tokenizer

To update the tokenizer with new training data:

1. Update `Sanskrit.txt` with new data
2. Delete `sanskrit_tokenizer.pkl`
3. Run `python train_tokenizer.py` locally
4. Commit the new `sanskrit_tokenizer.pkl`
5. Push to Hugging Face Spaces

## Support

For issues or questions, please open an issue on the Hugging Face Space repository.

