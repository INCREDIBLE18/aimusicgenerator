import argparse, os, json, numpy as np, yaml
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from src.utils.dataio import load_vocab, make_sequences
from src.models.rnn import build_rnn

# Enable mixed precision training for faster performance
try:
    policy = tf.keras.mixed_precision.Policy('mixed_float16')
    tf.keras.mixed_precision.set_global_policy(policy)
    print("Using mixed precision training")
except:
    print("Mixed precision training not available, using default")

# Optimize TensorFlow performance
tf.config.optimizer.set_jit(True)  # Enable XLA compilation
tf.data.experimental.enable_debug_mode()

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
    itos = {i:t for t,i in stoi.items()}
    ids = [stoi[t] for t in tokens if t in stoi]

    X_ids, y_ids = make_sequences(ids, seq_len)
    X = np.array(X_ids, dtype=np.int32)
    y = to_categorical(np.array(y_ids, dtype=np.int32), num_classes=len(stoi))

    model = build_rnn(vocab_size=len(stoi), seq_len=seq_len,
                      embedding_dim=cfg['model']['embedding_dim'],
                      rnn_units=cfg['model']['rnn_units'])
    
    # Use a more efficient optimizer with a higher learning rate
    optimizer = Adam(learning_rate=cfg['train']['learning_rate'] * 2)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy')

    out_dir = os.path.join('outputs', 'rnn')
    os.makedirs(out_dir, exist_ok=True)
    ckpt = ModelCheckpoint(os.path.join(out_dir, 'best.keras'), monitor='loss', save_best_only=True, verbose=1)
    rlr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=2, verbose=1)
    early_stop = EarlyStopping(monitor='loss', patience=4, verbose=1, restore_best_weights=True)
    
    # Convert to TF Dataset for better performance
    train_dataset = tf.data.Dataset.from_tensor_slices((X, y))
    train_dataset = train_dataset.shuffle(buffer_size=len(X)).batch(cfg['train']['batch_size']).prefetch(tf.data.AUTOTUNE)
    
    print(f"Training on {len(X)} sequences with vocab size {len(stoi)}")
    print(f"Batch size: {cfg['train']['batch_size']}, Epochs: {cfg['train']['epochs']}")
    
    model.fit(train_dataset, epochs=cfg['train']['epochs'], callbacks=[ckpt, rlr, early_stop])

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config.yaml')
    args = ap.parse_args()
    main(args.config)
