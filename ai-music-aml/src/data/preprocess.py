import argparse
import glob
import os
import pickle
from typing import List, Dict, Tuple

from music21 import converter, instrument, note, chord

from src.utils.dataio import save_vocab

def midi_to_events(midi_path: str):
    midi = converter.parse(midi_path)
    try:
        parts = instrument.partitionByInstrument(midi)
        elements = parts.parts[0].recurse()
    except Exception:
        elements = midi.flat.notes

    events = []
    prev_offset = None
    for el in elements:
        if isinstance(el, note.Note):
            pitch = str(el.pitch)
            dur = float(el.quarterLength)
            step = 0.0 if prev_offset is None else float(el.offset - prev_offset)
            prev_offset = float(el.offset)
            events.append({'pitch': pitch, 'duration': round(dur, 3), 'step': round(step, 3)})
        elif isinstance(el, chord.Chord):
            pitches = [str(n.pitch) for n in el.notes]
            dur = float(el.quarterLength)
            step = 0.0 if prev_offset is None else float(el.offset - prev_offset)
            prev_offset = float(el.offset)
            events.append({'pitch': pitches, 'duration': round(dur, 3), 'step': round(step, 3)})
    return events

def event_to_token(ev: dict) -> str:
    # Token: P<pitch>|D<dur>|S<step>  or  CHORD:p1,p2|D<dur>|S<step>
    pitch = ev['pitch']
    dur = ev['duration']
    step = ev['step']
    if isinstance(pitch, list):
        p = 'CHORD:' + ','.join(pitch)
    else:
        p = 'P' + pitch
    return f"{p}|D{dur}|S{step}"

def run(midi_dir: str, out_dir: str, min_notes: int = 100):
    os.makedirs(out_dir, exist_ok=True)
    all_tokens = []
    files = sorted(glob.glob(os.path.join(midi_dir, '*.mid'))) + sorted(glob.glob(os.path.join(midi_dir, '*.midi')))
    if not files:
        print('No MIDI files found in', midi_dir)
        return
    for f in files:
        events = midi_to_events(f)
        if len(events) < min_notes:
            continue
        tokens = [event_to_token(ev) for ev in events]
        all_tokens.extend(tokens + ['<SEP>'])  # separator token between songs

    # Build vocab
    vocab = sorted(set(all_tokens))
    stoi = {t: i for i, t in enumerate(vocab)}
    itos = {i: t for t, i in stoi.items()}

    # Save processed
    with open(os.path.join(out_dir, 'tokens.txt'), 'w', encoding='utf-8') as wf:
        wf.write('\n'.join(all_tokens))

    save_vocab(stoi, os.path.join(out_dir, 'vocab.json'))
    with open(os.path.join(out_dir, 'itos.pkl'), 'wb') as pf:
        pickle.dump(itos, pf)

    print(f'Processed {len(files)} files → {len(all_tokens)} tokens, vocab size={len(vocab)}')
    print('Saved to:', out_dir)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--midi_dir', required=True, help='Folder with .mid files')
    ap.add_argument('--out_dir', required=True, help='Output folder (e.g., outputs/processed)')
    ap.add_argument('--min_notes', type=int, default=100)
    args = ap.parse_args()
    run(args.midi_dir, args.out_dir, args.min_notes)
