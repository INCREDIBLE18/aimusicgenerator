import argparse, os, json, numpy as np, yaml
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical
from src.utils.dataio import load_vocab, make_sequences
from src.models.transformer import build_transformer

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
    y = to_categorical(np.array(y_ids, dtype=np.int32), num_classes=len(stoi))

    model = build_transformer(vocab_size=len(stoi), seq_len=seq_len,
                              d_model=cfg['model']['transformer']['d_model'],
                              num_layers=cfg['model']['transformer']['num_layers'],
                              num_heads=cfg['model']['transformer']['num_heads'],
                              dff=cfg['model']['transformer']['dff'],
                              dropout=cfg['model']['transformer']['dropout'])
    model.compile(optimizer='adam', loss='categorical_crossentropy')

    out_dir = os.path.join('outputs', 'transformer')
    os.makedirs(out_dir, exist_ok=True)
    ckpt = ModelCheckpoint(os.path.join(out_dir, 'best.keras'), monitor='loss', save_best_only=True, verbose=1)
    rlr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, verbose=1)

    model.fit(X, y, batch_size=cfg['train']['batch_size'], epochs=cfg['train']['epochs'], callbacks=[ckpt, rlr])

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config.yaml')
    args = ap.parse_args()
    main(args.config)
