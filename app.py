# -*- coding: utf-8 -*-
"""
BPE (Byte Pair Encoding) Tokenizer for Sanskrit
Gradio interface for Hugging Face Spaces
"""

import os
import json
import ast
import gradio as gr
from tokenizer import SanskritBPETokenizer


# Global tokenizer instance
tokenizer = None
TOKENIZER_PATH = "sanskrit_tokenizer.pkl"


def load_or_train_tokenizer():
    """Load tokenizer if exists, otherwise train it."""
    global tokenizer
    
    if os.path.exists(TOKENIZER_PATH):
        print("Loading pre-trained tokenizer...")
        tokenizer = SanskritBPETokenizer(vocab_size=5000, verbose=False)
        tokenizer.load(TOKENIZER_PATH)
        print(f"Tokenizer loaded! Vocabulary size: {len(tokenizer.vocab)}")
    else:
        print("Training new tokenizer...")
        if not os.path.exists('Sanskrit.txt'):
            return "Error: Sanskrit.txt file not found!"
        
        with open('Sanskrit.txt', 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
        
        tokenizer = SanskritBPETokenizer(vocab_size=5000, verbose=True)
        tokenizer.train(text)
        tokenizer.save(TOKENIZER_PATH)
        print(f"Tokenizer trained and saved! Vocabulary size: {len(tokenizer.vocab)}")
    
    return "Tokenizer ready!"


def encode_text(text):
    """Encode Sanskrit text using the tokenizer."""
    if tokenizer is None:
        return "Error: Tokenizer not loaded. Please wait for initialization."
    
    if not text.strip():
        return "Please enter some Sanskrit text to encode."
    
    try:
        encoded = tokenizer.encode(text)
        result = {
            "Token IDs": encoded,
            "Number of tokens": len(encoded),
            "Token IDs (string)": str(encoded)
        }
        return result
    except Exception as e:
        return {"Error": f"Error encoding text: {str(e)}"}


def decode_text(token_ids_str):
    """Decode token IDs back to Sanskrit text."""
    if tokenizer is None:
        return "Error: Tokenizer not loaded. Please wait for initialization."
    
    if not token_ids_str.strip():
        return "Please enter token IDs to decode (e.g., [256, 370, 401])."
    
    try:
        # Parse the token IDs string safely
        # Try JSON first, then ast.literal_eval as fallback
        try:
            token_ids = json.loads(token_ids_str)
        except:
            token_ids = ast.literal_eval(token_ids_str)
        
        if not isinstance(token_ids, list):
            return "Error: Token IDs must be a list of integers."
        
        # Ensure all elements are integers
        token_ids = [int(x) for x in token_ids]
        
        decoded = tokenizer.decode(token_ids)
        return decoded
    except Exception as e:
        return f"Error decoding tokens: {str(e)}. Please ensure token IDs are in format [256, 370, 401]"


def encode_and_decode(text):
    """Encode and decode text to show round-trip."""
    if tokenizer is None:
        return "Error: Tokenizer not loaded.", "Error: Tokenizer not loaded."
    
    if not text.strip():
        return "Please enter some Sanskrit text.", ""
    
    try:
        encoded = tokenizer.encode(text)
        decoded = tokenizer.decode(encoded)
        
        result = f"**Original text:** {text}\n\n"
        result += f"**Token IDs:** {encoded}\n\n"
        result += f"**Number of tokens:** {len(encoded)}\n\n"
        result += f"**Decoded text:** {decoded}\n\n"
        result += f"**Match:** {'✓ Yes' if text == decoded else '✗ No'}"
        
        return result, str(encoded)
    except Exception as e:
        return f"Error: {str(e)}", ""


# Initialize tokenizer on startup
print("Initializing Sanskrit BPE Tokenizer...")
status = load_or_train_tokenizer()
print(status)


# Create Gradio interface
with gr.Blocks(title="Sanskrit BPE Tokenizer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🕉️ Sanskrit BPE Tokenizer
    
    A Byte Pair Encoding (BPE) tokenizer trained on Sanskrit text with a vocabulary of 5000+ tokens.
    
    **Features:**
    - Encode Sanskrit text into token IDs
    - Decode token IDs back to Sanskrit text
    - Round-trip encoding/decoding with verification
    """)
    
    with gr.Tabs():
        with gr.TabItem("Encode Text"):
            gr.Markdown("### Encode Sanskrit text into token IDs")
            encode_input = gr.Textbox(
                label="Sanskrit Text",
                placeholder="Enter Sanskrit text here (e.g., एकवचनम्)",
                lines=5
            )
            encode_btn = gr.Button("Encode", variant="primary")
            encode_output = gr.JSON(label="Encoded Output", value={})
            
            encode_btn.click(
                fn=encode_text,
                inputs=encode_input,
                outputs=encode_output
            )
            
            encode_examples = gr.Examples(
                examples=[
                    ["एकवचनम्"],
                    ["लट् लकार: एकवचनम्"],
                    ["भगवान् धर्मनाथः"],
                ],
                inputs=encode_input
            )
        
        with gr.TabItem("Decode Tokens"):
            gr.Markdown("### Decode token IDs back to Sanskrit text")
            decode_input = gr.Textbox(
                label="Token IDs",
                placeholder="Enter token IDs as a list (e.g., [256, 370, 401, 273, 258])",
                lines=3
            )
            decode_btn = gr.Button("Decode", variant="primary")
            decode_output = gr.Textbox(label="Decoded Text", lines=3)
            
            decode_btn.click(
                fn=decode_text,
                inputs=decode_input,
                outputs=decode_output
            )
        
        with gr.TabItem("Encode & Decode"):
            gr.Markdown("### Encode and decode text (round-trip test)")
            roundtrip_input = gr.Textbox(
                label="Sanskrit Text",
                placeholder="Enter Sanskrit text here",
                lines=5
            )
            roundtrip_btn = gr.Button("Encode & Decode", variant="primary")
            roundtrip_output = gr.Markdown(label="Results")
            roundtrip_tokens = gr.Textbox(label="Token IDs", lines=2)
            
            roundtrip_btn.click(
                fn=encode_and_decode,
                inputs=roundtrip_input,
                outputs=[roundtrip_output, roundtrip_tokens]
            )
            
            roundtrip_examples = gr.Examples(
                examples=[
                    ["एकवचनम्"],
                    ["लट् लकार: एकवचनम् द्विवचनम्बहुवचनम्"],
                    ["भगवतः धर्मनाथस्य जन्म अभवत्"],
                ],
                inputs=roundtrip_input
            )
    
    gr.Markdown("""
    ### 📊 Tokenizer Information
    - **Vocabulary Size:** 5000 tokens
    - **Base Tokens:** 256 (UTF-8 bytes)
    - **Learned Merges:** 4744
    - **Compression Ratio:** ~30X
    
    ### 💡 Usage Tips
    - Enter Sanskrit text in Devanagari script
    - Token IDs are displayed as a list of integers
    - The tokenizer handles Unicode encoding automatically
    - Round-trip encoding/decoding should preserve the original text
    """)


if __name__ == "__main__":
    demo.launch(share=False)
