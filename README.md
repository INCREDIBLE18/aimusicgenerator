# 🎶 AI Music Composer (Advanced ML) – RNN + Transformer + GAN (+RL)

This project implements the full pipeline you requested:

```
Dataset (MIDI files)
       ⬇
Preprocessing (Pitch, Step, Duration → Tokens)
       ⬇
Baseline Model (RNN/LSTM) → Generates simple melody
       ⬇
Transformer Model → Adds structure & long-term patterns
       ⬇
GAN (Generator + Discriminator) → Refines for realism
       ⬇
(Optional RL Fine-tuning) → Improves harmony/quality
       ⬇
Generated Music (MIDI)
       ⬇
Visualization + Streamlit UI (Play, Download)
```

> Note: The GAN and RL components are provided as **working skeletons** to keep the repo concise. You can train the RNN/Transformer end-to-end out of the box, then optionally explore adversarial refinement and policy-gradients.

## � Quick Start

### Option 1: Modern Web UI (Recommended) ✨

The easiest way to use the AI Music Composer is through our beautiful web interface:

**Windows:**
```bash
# Double-click the launcher or run:
launch_studio.bat
```

**Cross-platform:**
```bash
python launch_studio.py
```

**Manual launch:**
```bash
cd ai-music-aml
streamlit run src/ui/modern_app.py
```

Then open http://localhost:8501 in your browser for a complete visual interface!

### Option 2: Command Line Interface 🖥️

For advanced users, use our CLI tool:

```bash
# Quick start (complete workflow)
python music_cli.py quickstart

# Individual commands
python music_cli.py status
python music_cli.py preprocess
python music_cli.py train --model rnn
python music_cli.py generate --model rnn --length 200
```

### Option 3: Manual Setup 🔧

## �📦 Manual Quickstart

1) **Install deps** (Python 3.10+ recommended):
```bash
pip install -r requirements.txt
```

2) **Add dataset**: Place `.mid` files into `midi_songs/`.

3) **Preprocess**:
```bash
# Using the config file (recommended)
python -m src.run_preprocess --config config.yaml --min_notes 200

# Or directly specifying paths
python -m src.data.preprocess --midi_dir d:\Music_Generator_Aiml\midi_songs --out_dir outputs --min_notes 200
```

4) **Train RNN baseline**:
```bash
python -m src.train_rnn --config config.yaml
```

5) **Train Transformer**:
```bash
python -m src.train_transformer --config config.yaml
```

6) **(Optional) Train GAN**:
```bash
python -m src.train_gan --config config.yaml
```

7) **(Optional) RL fine-tune**:
```bash
python -m src.fine_tune_rl --config config.yaml
```

8) **Generate MIDI** (choose model type: `rnn` or `transformer`):>
```bash
python -m src.generate --model_type rnn --checkpoint outputs/rnn/best.keras --out outputs/generated_rnn.mid
python -m src.generate --model_type transformer --checkpoint outputs/transformer/best.keras --out outputs/generated_transformer.mid
```

9) **Run UI** (Streamlit):
```bash
streamlit run src/ui/app.py
```

### 📁 Repo Layout
```
ai-music-aml/
├─ midi_songs/                 # MIDI files located at d:\Music_Generator_Aiml\midi_songs
├─ outputs/                    # checkpoints + processed data + generated MIDI
├─ src/
│  ├─ data/
│  │  └─ preprocess.py         # MIDI → events → token sequences
│  ├─ models/
│  │  ├─ rnn.py                # LSTM baseline
│  │  ├─ transformer.py        # Transformer model
│  │  └─ gan.py                # Simple sequence GAN (skeleton)
│  ├─ rl/
│  │  └─ reward.py             # simple music rewards + RL fine-tune utils
│  ├─ utils/
│  │  ├─ midi.py               # MIDI <-> events/tokens utilities
│  │  └─ dataio.py             # dataset loading helpers
│  ├─ ui/
│  │  └─ app.py                # Streamlit UI
│  ├─ train_rnn.py
│  ├─ train_transformer.py
│  ├─ train_gan.py
│  ├─ fine_tune_rl.py
│  └─ generate.py
├─ config.yaml
├─ requirements.txt
└─ README.md
```

## 🔬 Research Inspiration
- Eck & Schmidhuber (2002): LSTM for music improv.
- Boulanger-Lewandowski (2012): RNN-RBM for polyphonic music.
- Mogren (2016): C-RNN-GAN (GAN for music).
- Huang et al. (2018): Music Transformer.
- Hadjeres et al. (2017): DeepBach.

---

**Tip:** Start with `train_rnn.py` (fastest), verify generation, then move to `train_transformer.py`. After that, explore `train_gan.py` and `fine_tune_rl.py` to turn this into a full **Advanced ML** showcase.
