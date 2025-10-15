import argparse, os, numpy as np, yaml, tensorflow as tf
from tensorflow.keras.models import load_model
from src.utils.dataio import load_vocab
from src.utils.midi import save_midi_from_tokens

def temperature_sample(probs, temperature=1.0):
    probs = np.asarray(probs).astype('float64')
    if temperature <= 0:
        # argmax
        return int(np.argmax(probs))
    logits = np.log(probs + 1e-12) / temperature
    exp = np.exp(logits)
    probs = exp / np.sum(exp)
    return int(np.random.choice(len(probs), p=probs))

def main(model_type, checkpoint, out_path, config_path):
    cfg = yaml.safe_load(open(config_path, 'r'))
    seq_len = cfg['data']['sequence_length']
    gen_len = cfg['generate']['length']
    temp = cfg['generate']['temperature']

    stoi = load_vocab(os.path.join('outputs', 'processed', 'vocab.json'))
    itos = {i:t for t,i in stoi.items()}

    model = load_model(checkpoint, compile=False)

    # Seed sequence (random)
    seq = np.random.randint(0, len(stoi), size=(1, seq_len))

    tokens = []
    for _ in range(gen_len):
        logits = model.predict(seq, verbose=0)[0]
        probs = tf.nn.softmax(logits).numpy()
        idx = temperature_sample(probs, temperature=temp)
        tokens.append(itos[idx])
        seq = np.concatenate([seq[:,1:], np.array([[idx]])], axis=1)

    save_midi_from_tokens(tokens, out_path)
    print('Saved to', out_path)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--model_type', choices=['rnn','transformer'], default='rnn')
    ap.add_argument('--checkpoint', required=True)
    ap.add_argument('--out', default='outputs/generated.mid')
    ap.add_argument('--config', default='config.yaml')
    args = ap.parse_args()
    main(args.model_type, args.checkpoint, args.out, args.config)
