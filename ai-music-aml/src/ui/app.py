import streamlit as st
import os, yaml, numpy as np, tensorflow as tf
from tensorflow.keras.models import load_model
from src.utils.dataio import load_vocab
from src.utils.midi import save_midi_from_tokens

st.set_page_config(page_title='AI Music Composer', page_icon='🎶', layout='centered')
st.title('🎶 AI Music Composer (RNN + Transformer + GAN + RL)')

with st.expander('Instructions'):
    st.markdown('''
1. Place `.mid` files into `midi_songs/` and run preprocessing:
```bash
python -m src.data.preprocess --midi_dir midi_songs --out_dir outputs/processed
```
2. Train a model (RNN or Transformer):
```bash
python -m src.train_rnn --config config.yaml
# or
python -m src.train_transformer --config config.yaml
```
3. Select the trained checkpoint below and click **Generate**.
''')

cfg = yaml.safe_load(open('config.yaml', 'r'))
seq_len = cfg['data']['sequence_length']

model_type = st.selectbox('Model type', ['rnn', 'transformer'])
ckpt = st.text_input('Checkpoint path', value='outputs/rnn/best.keras')
length = st.slider('Length (notes)', min_value=50, max_value=600, value=200, step=10)
temperature = st.slider('Creativity (temperature)', min_value=0.1, max_value=2.0, value=1.0, step=0.1)
out_file = st.text_input('Output MIDI', value='outputs/ui_generated.mid')

def temperature_sample(probs, temperature=1.0):
    import numpy as np
    probs = np.asarray(probs).astype('float64')
    logits = np.log(probs + 1e-12) / temperature
    exp = np.exp(logits)
    probs = exp / np.sum(exp)
    return int(np.random.choice(len(probs), p=probs))

def generate_tokens(model, stoi, seq_len, gen_len, temp):
    import numpy as np, tensorflow as tf
    itos = {i:t for t,i in stoi.items()}
    seq = np.random.randint(0, len(stoi), size=(1, seq_len))
    tokens = []
    for _ in range(gen_len):
        logits = model.predict(seq, verbose=0)[0]
        probs = tf.nn.softmax(logits).numpy()
        idx = temperature_sample(probs, temperature=temp)
        tokens.append(itos[idx])
        seq = np.concatenate([seq[:,1:], np.array([[idx]])], axis=1)
    return tokens

if st.button('Generate 🎼'):
    try:
        model = load_model(ckpt, compile=False)
        stoi = load_vocab(os.path.join('outputs', 'processed', 'vocab.json'))
        toks = generate_tokens(model, stoi, seq_len, length, temperature)
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        save_midi_from_tokens(toks, out_file)
        st.success(f'Generated → {out_file}')
        st.audio(out_file)
        st.download_button('Download MIDI', data=open(out_file, 'rb').read(), file_name=os.path.basename(out_file))
    except Exception as e:
        st.error(str(e))
