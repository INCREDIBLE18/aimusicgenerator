from typing import List, Dict
from music21 import converter, instrument, note, chord, stream

def events_to_stream(events: List[dict]) -> stream.Stream:
    s = stream.Stream()
    offset = 0.0
    for ev in events:
        pitch = ev['pitch']
        dur = ev['duration']
        step = ev.get('step', 0.5)
        offset += step
        if isinstance(pitch, list): # chord
            notes = []
            for p in pitch:
                n = note.Note(p)
                n.quarterLength = dur
                n.storedInstrument = instrument.Piano()
                notes.append(n)
            c = chord.Chord(notes)
            c.offset = offset
            s.append(c)
        else:
            n = note.Note(pitch)
            n.quarterLength = dur
            n.offset = offset
            n.storedInstrument = instrument.Piano()
            s.append(n)
    return s

def tokens_to_events(tokens: List[str]):
    # Token format: P<pitch>|D<dur>|S<step> or CHORD:p1,p2|D<dur>|S<step>
    events = []
    for t in tokens:
        parts = t.split('|')
        pitch_part = parts[0]
        dur = float(parts[1][1:]) if parts[1].startswith('D') else float(parts[1])
        step = float(parts[2][1:]) if parts[2].startswith('S') else float(parts[2])
        if pitch_part.startswith('CHORD:'):
            pitches = [p for p in pitch_part.replace('CHORD:', '').split(',') if p]
            events.append({'pitch': pitches, 'duration': dur, 'step': step})
        else:
            pitch = pitch_part[1:] if pitch_part.startswith('P') else pitch_part
            events.append({'pitch': pitch, 'duration': dur, 'step': step})
    return events

def save_midi_from_tokens(tokens: List[str], out_path: str):
    events = tokens_to_events(tokens)
    s = events_to_stream(events)
    s.write('midi', fp=out_path)
