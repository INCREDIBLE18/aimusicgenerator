from tensorflow.keras import layers, models

def build_rnn(vocab_size: int, seq_len: int, embedding_dim: int = 256, rnn_units: int = 512):
    inp = layers.Input(shape=(seq_len,), dtype='int32')
    x = layers.Embedding(vocab_size, embedding_dim)(inp)
    # Simplified: Use a single LSTM layer with more units instead of stacked LSTM
    x = layers.LSTM(rnn_units)(x)
    x = layers.Dropout(0.3)(x)
    out = layers.Dense(vocab_size, activation='softmax')(x)
    model = models.Model(inp, out)
    return model
