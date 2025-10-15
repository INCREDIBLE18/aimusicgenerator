import argparse, os, json, numpy as np, yaml
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from src.utils.dataio import load_vocab, make_sequences
from src.models.gan import SeqGAN

def load_tokens_and_vocab(proc_dir):
    with open(os.path.join(proc_dir, 'tokens.txt'), 'r', encoding='utf-8') as f:
        tokens = [line.strip() for line in f if line.strip()]
    vocab = load_vocab(os.path.join(proc_dir, 'vocab.json'))
    return tokens, vocab

def main(config_path):
    cfg = yaml.safe_load(open(config_path, 'r'))
    proc_dir = cfg['data']['processed_dir']
    seq_len = cfg['data']['sequence_length']

    tokens, vocab = load_tokens_and_vocab(proc_dir)
    stoi = vocab
    ids = [stoi[t] for t in tokens if t in stoi]

    X_ids, y_ids = make_sequences(ids, seq_len)
    X = np.array(X_ids, dtype=np.int32)
    # Build one-hot sequences as 'real' samples for discriminator
    X_oh = to_categorical(X, num_classes=len(stoi))
    # For simplicity, collapse time by averaging across time to (batch, seq_len, vocab) via repeat
    # (We keep the time dimension; discriminator is designed for (batch, seq_len, vocab))
    dataset = tf.data.Dataset.from_tensor_slices(X_oh).shuffle(2048).batch(32).prefetch(tf.data.AUTOTUNE)

    gan = SeqGAN(vocab_size=len(stoi), seq_len=seq_len, temperature=1.0)
    gan.compile()
    out_dir = os.path.join('outputs', 'gan')
    os.makedirs(out_dir, exist_ok=True)

    for epoch in range(5):  # keep short (you can increase)
        for batch in dataset:
            metrics = gan.train_step(batch)
        print(f"Epoch {epoch+1}:", {k: float(v.numpy()) for k, v in metrics.items()})

    gan.gen.save(os.path.join(out_dir, 'generator.keras'))
    gan.disc.save(os.path.join(out_dir, 'discriminator.keras'))
    print('Saved GAN components.')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config.yaml')
    args = ap.parse_args()
    main(args.config)
