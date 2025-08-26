from tensorflow.keras import layers, models
import tensorflow as tf

class PositionalEncoding(layers.Layer):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        import numpy as np
        pos = np.arange(max_len)[:, None]
        i = np.arange(d_model)[None, :]
        angle_rates = 1 / (10000 ** (2 * (i//2) / d_model))
        angle_rads = pos * angle_rates
        pe = np.zeros((max_len, d_model))
        pe[:, 0::2] = np.sin(angle_rads[:, 0::2])
        pe[:, 1::2] = np.cos(angle_rads[:, 1::2])
        self.pe = tf.constant(pe[None, ...], dtype=tf.float32)

    def call(self, x):
        seq_len = tf.shape(x)[1]
        return x + self.pe[:, :seq_len, :]

def transformer_block(x, num_heads, dff, dropout):
    attn = layers.MultiHeadAttention(num_heads=num_heads, key_dim=x.shape[-1])(x, x)
    x = layers.LayerNormalization(epsilon=1e-6)(x + attn)
    ffn = layers.Dense(dff, activation='relu')(x)
    ffn = layers.Dense(x.shape[-1])(ffn)
    x = layers.LayerNormalization(epsilon=1e-6)(x + ffn)
    if dropout:
        x = layers.Dropout(dropout)(x)
    return x

def build_transformer(vocab_size: int, seq_len: int, d_model: int = 256, num_layers: int = 4, num_heads: int = 4, dff: int = 512, dropout: float = 0.1):
    inp = layers.Input(shape=(seq_len,), dtype='int32')
    x = layers.Embedding(vocab_size, d_model)(inp)
    x = PositionalEncoding(d_model)(x)
    for _ in range(num_layers):
        x = transformer_block(x, num_heads=num_heads, dff=dff, dropout=dropout)
    x = layers.GlobalAveragePooling1D()(x)
    out = layers.Dense(vocab_size, activation='softmax')(x)
    return models.Model(inp, out)
