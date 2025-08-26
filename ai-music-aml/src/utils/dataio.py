import json
import os
from typing import Dict, List, Tuple

def load_vocab(vocab_path: str) -> Dict[str, int]:
    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    return vocab

def save_vocab(vocab: dict, vocab_path: str):
    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

def make_sequences(tokens: list, seq_len: int):
    X, y = [], []
    for i in range(0, len(tokens) - seq_len):
        X.append(tokens[i:i+seq_len])
        y.append(tokens[i+seq_len])
    return X, y
