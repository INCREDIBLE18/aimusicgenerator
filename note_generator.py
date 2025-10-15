#!/usr/bin/env python3
"""
Note-Based Music Generator
Generate AI music starting with specific notes or chords
"""

import sys
import os
import json
import pickle
import numpy as np
import tensorflow as tf
from music21 import stream, note, chord, duration, tempo, meter

def generate_with_seed_notes(seed_notes, length=200, creativity=1.0, output_file="seeded_song.mid"):
    """
    Generate music starting with specific notes
    
    Args:
        seed_notes: List like ["C4", "E4", "G4"] or chord names like ["C", "Am", "F", "G"]
        length: Number of tokens to generate
        creativity: Temperature for randomness (0.1-2.0)
        output_file: Output filename
    """
    
    print(f"🎼 Note-Based AI Music Generator")
    print(f"🎵 Seed notes: {seed_notes}")
    print(f"📏 Length: {length} tokens")
    print(f"🌡️ Creativity: {creativity}")
    print(f"📁 Output: {output_file}")
    print("=" * 50)
    
    print(f"🧠 Loading AI model...")
    
    try:
        # Load model and data
        model = tf.keras.models.load_model('ai-music-aml/outputs/rnn/best.keras')
        
        with open('ai-music-aml/outputs/processed/vocab.json', 'r') as f:
            vocab = json.load(f)
        
        with open('ai-music-aml/outputs/processed/itos.pkl', 'rb') as f:
            itos = pickle.load(f)
        
        stoi = {v: k for k, v in itos.items()}
        
        print(f"✅ Model loaded. Vocabulary size: {len(vocab)}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
    
    # Convert seed notes to tokens
    print(f"🔄 Converting seed notes to AI tokens...")
    seed_tokens = convert_notes_to_tokens(seed_notes, stoi, vocab)
    
    if not seed_tokens:
        print("⚠️ Could not convert any seed notes, using random start")
        seed_tokens = [np.random.randint(0, len(vocab)) for _ in range(4)]
    else:
        print(f"✅ Converted {len(seed_tokens)} seed notes to tokens")
    
    print(f"🎼 Generating {length} tokens with creativity {creativity}...")
    
    # Generate sequence
    generated = generate_music_sequence(model, seed_tokens, length, creativity, itos)
    
    # Create MIDI
    print(f"🎵 Creating MIDI file...")
    success = tokens_to_midi_advanced(generated, itos, output_file)
    
    if success:
        file_size = os.path.getsize(f'outputs/{output_file}')
        print(f"\n🎉 SUCCESS!")
        print(f"✅ Generated: outputs/{output_file}")
        print(f"📊 File size: {file_size} bytes")
        print(f"🎵 Starting notes: {seed_notes}")
        print(f"📏 Total tokens: {len(generated)}")
        print(f"💡 Try playing the MIDI file in any music player!")
        return True
    else:
        print("❌ Failed to create MIDI")
        return False

def convert_notes_to_tokens(seed_notes, stoi, vocab):
    """Convert note names to vocabulary tokens"""
    tokens = []
    
    print("🔍 Looking for notes in AI vocabulary...")
    
    for note_name in seed_notes:
        # Try different token formats that might exist in the vocabulary
        possible_tokens = [
            f"P{note_name}|D0.5|S0.0",      # Single note format
            f"P{note_name}|D0.25|S0.0",     # Shorter duration
            f"P{note_name}|D1.0|S0.0",      # Longer duration
            f"CHORD:{note_name}|D0.5|S0.0", # Chord format
            f"NOTE:{note_name}",             # Simple note format
            f"{note_name}",                  # Direct note name
            f"note_{note_name}",             # Prefixed note
            f"pitch_{note_name}"             # Pitch format
        ]
        
        # Also try with different octaves if not specified
        if len(note_name) == 1 or (len(note_name) == 2 and '#' in note_name):
            for octave in [3, 4, 5]:
                possible_tokens.append(f"P{note_name}{octave}|D0.5|S0.0")
                possible_tokens.append(f"P{note_name}{octave}|D0.25|S0.0")
        
        found = False
        for token in possible_tokens:
            if token in stoi:
                tokens.append(stoi[token])
                print(f"  ✅ {note_name} → {token}")
                found = True
                break
        
        if not found:
            print(f"  🔍 Searching for similar patterns to {note_name}...")
            # Use a token that contains the note name
            matching_tokens = [k for k in stoi.keys() if note_name.upper() in k.upper()]
            if matching_tokens:
                chosen = matching_tokens[0]
                tokens.append(stoi[chosen])
                print(f"  🔄 Using similar: {note_name} → {chosen}")
            else:
                print(f"  ⚠️ {note_name} not found, skipping")
    
    return tokens

def generate_music_sequence(model, seed_tokens, length, temperature, itos):
    """Generate music sequence with seed"""
    sequence = seed_tokens.copy()
    vocab_size = len(itos)
    
    for i in range(length - len(seed_tokens)):
        # Prepare input (use last 64 tokens as model expects)
        input_seq = sequence[-64:] if len(sequence) >= 64 else sequence
        if len(input_seq) < 64:
            input_seq = input_seq + [0] * (64 - len(input_seq))
        
        # Predict next token
        prediction = model.predict(np.array([input_seq]), verbose=0)[0]
        
        # Apply temperature for creativity control
        if temperature != 1.0:
            prediction = np.log(prediction + 1e-8) / temperature
            prediction = np.exp(prediction)
        
        # Normalize probabilities
        prediction = prediction / np.sum(prediction)
        
        # Sample next token
        next_token = np.random.choice(vocab_size, p=prediction)
        sequence.append(next_token)
        
        # Progress indicator
        if (i + 1) % 25 == 0:
            progress = (i + 1) / (length - len(seed_tokens)) * 100
            print(f"  Progress: {progress:.0f}% ({i + 1}/{length - len(seed_tokens)} tokens)")
    
    return sequence

def tokens_to_midi_advanced(tokens, itos, output_file):
    """Convert tokens to MIDI with advanced parsing"""
    try:
        score = stream.Stream()
        score.append(tempo.MetronomeMark(number=120))
        score.append(meter.TimeSignature('4/4'))
        
        current_time = 0
        note_count = 0
        chord_count = 0
        
        for token_idx in tokens:
            token = itos.get(token_idx, "")
            
            # Parse single notes (P format)
            if token.startswith("P") and "|D" in token:
                try:
                    # Parse P{note}|D{duration}|S{start}
                    parts = token.split("|")
                    note_part = parts[0][1:]  # Remove 'P'
                    duration_val = float(parts[1][1:]) if len(parts) > 1 else 0.5  # Remove 'D'
                    
                    n = note.Note(note_part)
                    n.duration.quarterLength = max(0.125, min(4.0, duration_val))
                    n.offset = current_time
                    score.append(n)
                    
                    current_time += n.duration.quarterLength
                    note_count += 1
                    
                except Exception as e:
                    pass
                    
            # Parse chords (CHORD format)
            elif token.startswith("CHORD:") and "|D" in token:
                try:
                    # Parse CHORD:{notes}|D{duration}|S{start}
                    parts = token.split("|")
                    chord_part = parts[0][6:]  # Remove 'CHORD:'
                    duration_val = float(parts[1][1:]) if len(parts) > 1 else 0.5  # Remove 'D'
                    
                    chord_notes = chord_part.split(",")
                    c = chord.Chord(chord_notes)
                    c.duration.quarterLength = max(0.125, min(4.0, duration_val))
                    c.offset = current_time
                    score.append(c)
                    
                    current_time += c.duration.quarterLength
                    chord_count += 1
                    
                except Exception as e:
                    pass
        
        # Add some default notes if nothing was parsed
        if note_count == 0 and chord_count == 0:
            print("🎵 Adding default melody as fallback...")
            default_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
            for i, note_name in enumerate(default_notes):
                n = note.Note(note_name, quarterLength=0.5)
                n.offset = i * 0.5
                score.append(n)
            note_count = len(default_notes)
        
        # Ensure output directory exists
        os.makedirs('outputs', exist_ok=True)
        
        # Write MIDI file
        score.write('midi', fp=f'outputs/{output_file}')
        
        print(f"🎵 Musical elements created: {note_count} notes, {chord_count} chords")
        return True
        
    except Exception as e:
        print(f"❌ MIDI creation error: {e}")
        return False

def show_usage():
    """Show usage examples"""
    print("🎵 Note-Based AI Music Generator")
    print("=" * 50)
    print("\nUsage:")
    print("  py -3 note_generator.py <notes> [length] [creativity] [output]")
    print("\n📝 Examples:")
    print("  py -3 note_generator.py \"C4 E4 G4\"")
    print("  py -3 note_generator.py \"C4,E4,G4,C5\" 150 1.2")
    print("  py -3 note_generator.py \"C4 D4 E4 F4\" 200 0.8 my_melody.mid")
    print("  py -3 note_generator.py \"A4 B4 C5 D5\" 300 1.5 scale_song.mid")
    print("\n🎹 Note Formats:")
    print("  Single notes: C4, D#4, F5, G3")
    print("  Multiple notes: \"C4 E4 G4\" or \"C4,E4,G4\"")
    print("  Chord names: \"C Em F G\" (experimental)")
    print("\n⚙️ Parameters:")
    print("  notes: Note names (required)")
    print("  length: Tokens to generate (default: 200)")
    print("  creativity: 0.1 (conservative) to 2.0 (very creative, default: 1.0)")
    print("  output: Filename (default: seeded_song.mid)")
    print("\n🎯 Creativity Guide:")
    print("  0.1-0.5: Very conservative, stays close to training")
    print("  0.6-0.9: Balanced, good musical structure")
    print("  1.0-1.3: Creative, interesting variations")
    print("  1.4-2.0: Experimental, more unpredictable")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    # Parse arguments
    notes_input = sys.argv[1]
    length = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    creativity = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    output_file = sys.argv[4] if len(sys.argv) > 4 else "seeded_song.mid"
    
    # Validate parameters
    if length < 10 or length > 1000:
        print("❌ Length must be between 10 and 1000")
        sys.exit(1)
    
    if creativity < 0.1 or creativity > 2.0:
        print("❌ Creativity must be between 0.1 and 2.0")
        sys.exit(1)
    
    # Parse notes (handle comma or space separated)
    if "," in notes_input:
        notes = [n.strip() for n in notes_input.split(",")]
    else:
        notes = notes_input.split()
    
    if not notes:
        print("❌ No notes provided")
        sys.exit(1)
    
    # Generate music
    success = generate_with_seed_notes(notes, length, creativity, output_file)
    sys.exit(0 if success else 1)