import argparse, os, json, numpy as np, yaml, tensorflow as tf
from tensorflow.keras.models import load_model
from src.utils.dataio import load_vocab
from src.rl.reward import in_scale, rhythm_stability

def sample_with_temperature(logits, temperature=1.0):
    logits = logits / temperature
    p = tf.nn.softmax(logits).numpy()
    return np.random.choice(len(p), p=p)

def main(config_path, checkpoint, proc_dir, out_path, episodes=1000, temperature=1.0):
    cfg = yaml.safe_load(open(config_path, 'r'))
    stoi = load_vocab(os.path.join(proc_dir, 'vocab.json'))
    itos = {i:t for t,i in stoi.items()}

    model = load_model(checkpoint)
    seq_len = cfg['data']['sequence_length']

    # Initialize with random sequences
    seq = np.random.randint(0, len(stoi), size=(1, seq_len))

    opt = tf.keras.optimizers.Adam(1e-5)

    for ep in range(episodes):
        with tf.GradientTape() as tape:
            logits = model(seq, training=True)
            idx = sample_with_temperature(logits[0], temperature)
            tok = itos[idx]
            # reward signal
            parts = tok.split('|')
            r = 0.5 * in_scale(parts[0]) + 0.5 * rhythm_stability(parts[1], parts[2])
            # simple objective: encourage higher prob for rewarded token
            prob = tf.nn.softmax(logits)[0, idx]
            loss = -tf.math.log(prob + 1e-9) * (r - 0.5)  # baseline 0.5
        grads = tape.gradient(loss, model.trainable_variables)
        opt.apply_gradients(zip(grads, model.trainable_variables))

        seq = np.concatenate([seq[:,1:], np.array([[idx]])], axis=1)
        if (ep+1) % 100 == 0:
            print(f"Episode {ep+1}, reward={r:.3f}")

    model.save(out_path)
    print('Saved RL fine-tuned model to', out_path)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config.yaml')
    ap.add_argument('--checkpoint', required=True, help='Path to base model (keras)')
    ap.add_argument('--proc_dir', default='outputs/processed')
    ap.add_argument('--out', default='outputs/rl_finetuned.keras')
    ap.add_argument('--episodes', type=int, default=500)
    ap.add_argument('--temperature', type=float, default=1.0)
    args = ap.parse_args()
    main(args.config, args.checkpoint, args.proc_dir, args.out, args.episodes, args.temperature)
