# 🎵 AI Music Generator# 🎶 AI Music Composer (Advanced ML) – RNN + Transformer + GAN (+RL)



A deep learning project that generates music using advanced neural networks including LSTM, Transformer, and GAN models.This project implements the full pipeline you requested:



## Features```

Dataset (MIDI files)

- **Multiple Generation Modes**: Random, note-based, chord progression, and style-based generation       ⬇

- **Web Interface**: Streamlit-based professional UIPreprocessing (Pitch, Step, Duration → Tokens)

- **Command Line Tools**: Multiple generators for different use cases       ⬇

- **Advanced ML Models**: LSTM, Transformer, and GAN architecturesBaseline Model (RNN/LSTM) → Generates simple melody

       ⬇

## Quick StartTransformer Model → Adds structure & long-term patterns

       ⬇

### Web InterfaceGAN (Generator + Discriminator) → Refines for realism

```bash       ⬇

python launch_studio.py(Optional RL Fine-tuning) → Improves harmony/quality

```       ⬇

Generated Music (MIDI)

### Command Line Examples       ⬇

```bashVisualization + Streamlit UI (Play, Download)

# Basic generation```

python advanced_music_gen.py 200 1.0 my_song.mid

> Note: The GAN and RL components are provided as **working skeletons** to keep the repo concise. You can train the RNN/Transformer end-to-end out of the box, then optionally explore adversarial refinement and policy-gradients.

# Chord-based generation

python chord_generator_v2.py jazz 300 0.8 jazz_song.mid## � Quick Start



# Note-based generation### Option 1: Modern Web UI (Recommended) ✨

python note_generator.py "C4 E4 G4" 150 1.0 chord_song.mid

The easiest way to use the AI Music Composer is through our beautiful web interface:

# Ultimate generator

python ultimate_music.py style happy 250 1.0**Windows:**

``````bash

# Double-click the launcher or run:

## Requirementslaunch_studio.bat

```

- Python 3.8+

- TensorFlow 2.x**Cross-platform:**

- Music21```bash

- Streamlitpython launch_studio.py

- NumPy```



## Installation**Manual launch:**

```bash

```bashcd ai-music-aml

git clone https://github.com/INCREDIBLE18/aimusicgenerator.gitstreamlit run src/ui/modern_app.py

cd aimusicgenerator```

pip install -r requirements.txt

```Then open http://localhost:8501 in your browser for a complete visual interface!



## Model Architecture### Option 2: Command Line Interface 🖥️



- **LSTM Networks**: Sequential music modeling with memory gatesFor advanced users, use our CLI tool:

- **Transformer**: Self-attention for parallel processing

- **GAN**: Adversarial training for creative generation```bash

- **Advanced Sampling**: Temperature and nucleus sampling techniques# Quick start (complete workflow)

python music_cli.py quickstart

## Generated Output

# Individual commands

- Standard MIDI files (.mid)python music_cli.py status

- Compatible with any MIDI player or DAWpython music_cli.py preprocess

- Configurable length, creativity, and style parameterspython music_cli.py train --model rnn

python music_cli.py generate --model rnn --length 200

---```



**Create AI music today!** 🎶### Option 3: Manual Setup 🔧

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
