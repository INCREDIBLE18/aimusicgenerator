"""A minimal sequence GAN skeleton using Gumbel-Softmax for discrete tokens.
This is intentionally compact to keep the project runnable. Consider it a starting point.
"""
import tensorflow as tf
from tensorflow.keras import layers, models

def sample_gumbel(shape, eps=1e-20):
    U = tf.random.uniform(shape, minval=0, maxval=1)
    return -tf.math.log(-tf.math.log(U + eps) + eps)

def gumbel_softmax_sample(logits, temperature):
    y = logits + sample_gumbel(tf.shape(logits))
    return tf.nn.softmax(y / temperature)

def build_generator(vocab_size: int, seq_len: int, d_model: int = 256, rnn_units: int = 256):
    inp = layers.Input(shape=(seq_len,), dtype='int32')
    x = layers.Embedding(vocab_size, d_model)(inp)
    x = layers.LSTM(rnn_units, return_sequences=True)(x)
    x = layers.LSTM(rnn_units)(x)
    logits = layers.Dense(vocab_size)(x)
    model = models.Model(inp, logits, name='generator')
    return model

def build_discriminator(vocab_size: int, seq_len: int, d_model: int = 256):
    inp = layers.Input(shape=(seq_len,), dtype='float32') # one-hot / soft one-hot
    x = layers.Conv1D(128, 5, padding='same', activation='relu')(inp)
    x = layers.MaxPool1D(2)(x)
    x = layers.Conv1D(128, 3, padding='same', activation='relu')(x)
    x = layers.GlobalMaxPool1D()(x)
    x = layers.Dense(128, activation='relu')(x)
    out = layers.Dense(1, activation='sigmoid')(x)
    return models.Model(inp, out, name='discriminator')

class SeqGAN(tf.keras.Model):
    def __init__(self, vocab_size, seq_len, temperature=1.0):
        super().__init__()
        self.vocab_size = vocab_size
        self.seq_len = seq_len
        self.temperature = temperature
        self.gen = build_generator(vocab_size, seq_len)
        self.disc = build_discriminator(vocab_size, seq_len)
        self.gen_opt = tf.keras.optimizers.Adam(1e-4)
        self.disc_opt = tf.keras.optimizers.Adam(1e-4)

    def compile(self, **kwargs):
        super().compile(**kwargs)
        self.bce = tf.keras.losses.BinaryCrossentropy(from_logits=False)

    def train_step(self, data):
        real = data  # real is expected already as (batch, seq_len, vocab_size) one-hot
        batch_size = tf.shape(real)[0]

        # --------------------- Train Discriminator ---------------------
        with tf.GradientTape() as tape:
            # fake logits -> gumbel-softmax to get soft one-hot
            z = tf.random.uniform((batch_size, self.seq_len), maxval=self.vocab_size, dtype=tf.int32)
            fake_logits = self.gen(z)
            fake_probs = tf.nn.softmax(fake_logits)  # (batch, vocab)
            # repeat token to sequence shape (simple toy: same token repeated)
            fake_seq = tf.tile(fake_probs[:, None, :], [1, self.seq_len, 1])
            real_pred = self.disc(real)
            fake_pred = self.disc(fake_seq)
            d_loss = self.bce(tf.ones_like(real_pred), real_pred) + self.bce(tf.zeros_like(fake_pred), fake_pred)
        grads = tape.gradient(d_loss, self.disc.trainable_variables)
        self.disc_opt.apply_gradients(zip(grads, self.disc.trainable_variables))

        # --------------------- Train Generator ---------------------
        with tf.GradientTape() as tape:
            z = tf.random.uniform((batch_size, self.seq_len), maxval=self.vocab_size, dtype=tf.int32)
            fake_logits = self.gen(z)
            fake_probs = tf.nn.softmax(fake_logits)
            fake_seq = tf.tile(fake_probs[:, None, :], [1, self.seq_len, 1])
            fake_pred = self.disc(fake_seq)
            g_loss = self.bce(tf.ones_like(fake_pred), fake_pred)
        grads = tape.gradient(g_loss, self.gen.trainable_variables)
        self.gen_opt.apply_gradients(zip(grads, self.gen.trainable_variables))

        return {'d_loss': d_loss, 'g_loss': g_loss}
