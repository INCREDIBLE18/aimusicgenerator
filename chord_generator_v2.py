#!/usr/bin/env python3
"""
Advanced Chord Progression Generator
Generate AI music with specific chord progressions
Compatible version without dependency issues
"""

import sys
import os
import json
import pickle
import numpy as np

# Common chord mappings
CHORD_NOTES = {
    # Major chords
    'C': ['C4', 'E4', 'G4'],
    'D': ['D4', 'F#4', 'A4'],
    'E': ['E4', 'G#4', 'B4'],
    'F': ['F4', 'A4', 'C5'],
    'G': ['G4', 'B4', 'D5'],
    'A': ['A4', 'C#5', 'E5'],
    'B': ['B4', 'D#5', 'F#5'],
    
    # Minor chords
    'Cm': ['C4', 'E-4', 'G4'],
    'Dm': ['D4', 'F4', 'A4'],
    'Em': ['E4', 'G4', 'B4'],
    'Fm': ['F4', 'A-4', 'C5'],
    'Gm': ['G4', 'B-4', 'D5'],
    'Am': ['A4', 'C5', 'E5'],
    'Bm': ['B4', 'D5', 'F#5'],
    
    # Seventh chords
    'C7': ['C4', 'E4', 'G4', 'B-4'],
    'Cmaj7': ['C4', 'E4', 'G4', 'B4'],
    'Dm7': ['D4', 'F4', 'A4', 'C5'],
    'Em7': ['E4', 'G4', 'B4', 'D5'],
    'Fmaj7': ['F4', 'A4', 'C5', 'E5'],
    'G7': ['G4', 'B4', 'D5', 'F5'],
    'Am7': ['A4', 'C5', 'E5', 'G5'],
    
    # Common progressions shortcuts
    'I': ['C4', 'E4', 'G4'],    # Tonic
    'ii': ['D4', 'F4', 'A4'],   # Supertonic minor
    'iii': ['E4', 'G4', 'B4'],  # Mediant minor
    'IV': ['F4', 'A4', 'C5'],   # Subdominant
    'V': ['G4', 'B4', 'D5'],    # Dominant
    'vi': ['A4', 'C5', 'E5'],   # Submediant minor
    'vii°': ['B4', 'D5', 'F5']  # Leading tone diminished
}

# Popular progressions
PROGRESSIONS = {
    'pop': ['C', 'Am', 'F', 'G'],
    'jazz': ['Cmaj7', 'Am7', 'Dm7', 'G7'],
    'blues': ['C7', 'F7', 'C7', 'G7'],
    'folk': ['C', 'F', 'Am', 'G'],
    'rock': ['C', 'G', 'Am', 'F'],
    'minor': ['Am', 'F', 'C', 'G'],
    'sad': ['Am', 'Dm', 'G', 'C'],
    'happy': ['C', 'F', 'G', 'C'],
    'classical': ['C', 'G', 'Am', 'F', 'C', 'Dm', 'G', 'C']
}

def generate_chord_progression_song(progression_input, length=250, creativity=1.0, tempo_bpm=120, output_file="chord_song.mid"):
    """
    Generate music based on chord progression
    """
    
    print(f"🎼 Advanced Chord Progression Generator")
    print(f"🎵 Progression: {progression_input}")
    print(f"📏 Length: {length} tokens")
    print(f"🌡️ Creativity: {creativity}")
    print(f"🎶 Tempo: {tempo_bpm} BPM")
    print(f"📁 Output: {output_file}")
    print("=" * 50)
    
    # Parse chord progression
    chord_progression = parse_chord_progression(progression_input)
    print(f"🎹 Parsed chords: {chord_progression}")
    
    # Convert to note sequences
    note_sequences = []
    for chord_name in chord_progression:
        if chord_name in CHORD_NOTES:
            note_sequences.extend(CHORD_NOTES[chord_name])
        else:
            print(f"⚠️ Unknown chord: {chord_name}, skipping")
    
    if not note_sequences:
        print("❌ No valid chords found")
        return False
    
    print(f"🎵 Generated note sequence: {note_sequences[:10]}{'...' if len(note_sequences) > 10 else ''}")
    
    # Load AI model
    print(f"🧠 Loading AI model...")
    try:
        # Import TensorFlow dynamically to avoid version issues
        import tensorflow as tf
        
        # Try different ways to load the model
        model = None
        try:
            model = tf.keras.models.load_model('ai-music-aml/outputs/rnn/best.keras')
        except:
            try:
                from tensorflow.keras import models
                model = models.load_model('ai-music-aml/outputs/rnn/best.keras')
            except:
                print("❌ Could not load TensorFlow model")
                return False
        
        with open('ai-music-aml/outputs/processed/vocab.json', 'r') as f:
            vocab = json.load(f)
        
        with open('ai-music-aml/outputs/processed/itos.pkl', 'rb') as f:
            itos = pickle.load(f)
        
        stoi = {v: k for k, v in itos.items()}
        print(f"✅ Model loaded. Vocabulary size: {len(vocab)}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("💡 Falling back to basic note pattern generation...")
        return generate_chord_pattern_fallback(chord_progression, output_file)
    
    # Convert chord notes to tokens
    seed_tokens = convert_chord_notes_to_tokens(note_sequences, stoi)
    
    if not seed_tokens:
        print("⚠️ Could not convert chord notes, using random seed")
        seed_tokens = [np.random.randint(0, len(vocab)) for _ in range(8)]
    
    # Generate extended sequence
    print(f"🎼 Generating music based on chord progression...")
    generated = generate_chord_based_sequence(model, seed_tokens, length, creativity, itos)
    
    # Create advanced MIDI with chord progression
    print(f"🎵 Creating advanced MIDI file...")
    success = create_chord_progression_midi(generated, itos, chord_progression, tempo_bpm, output_file)
    
    if success:
        file_size = os.path.getsize(f'outputs/{output_file}')
        print(f"\n🎉 SUCCESS!")
        print(f"✅ Generated: outputs/{output_file}")
        print(f"📊 File size: {file_size} bytes")
        print(f"🎹 Chord progression: {' → '.join(chord_progression)}")
        print(f"📏 Total tokens: {len(generated)}")
        print(f"🎶 Tempo: {tempo_bpm} BPM")
        print(f"💡 Try playing the MIDI file in any music player!")
        return True
    else:
        print("❌ Failed to create MIDI")
        return False

def generate_chord_pattern_fallback(chord_progression, output_file):
    """Fallback: Generate basic chord pattern without AI model"""
    print("🎵 Generating basic chord pattern...")
    
    try:
        from music21 import stream, note, chord, tempo
        
        score = stream.Stream()
        score.append(tempo.MetronomeMark(number=120))
        
        current_time = 0
        for i, chord_name in enumerate(chord_progression * 4):  # Repeat progression
            if chord_name in CHORD_NOTES:
                chord_notes = CHORD_NOTES[chord_name]
                c = chord.Chord(chord_notes)
                c.duration.quarterLength = 1.0
                c.offset = current_time
                score.append(c)
                current_time += 1.0
        
        # Ensure output directory exists
        os.makedirs('outputs', exist_ok=True)
        
        # Write MIDI file
        score.write('midi', fp=f'outputs/{output_file}')
        
        file_size = os.path.getsize(f'outputs/{output_file}')
        print(f"\n🎉 Fallback SUCCESS!")
        print(f"✅ Generated: outputs/{output_file}")
        print(f"📊 File size: {file_size} bytes")
        print(f"🎹 Basic chord pattern: {' → '.join(chord_progression)}")
        return True
        
    except Exception as e:
        print(f"❌ Fallback generation failed: {e}")
        return False

def parse_chord_progression(progression_input):
    """Parse various chord progression formats"""
    
    # Check if it's a predefined progression
    if progression_input.lower() in PROGRESSIONS:
        return PROGRESSIONS[progression_input.lower()]
    
    # Parse as chord list
    if ',' in progression_input:
        chords = [c.strip() for c in progression_input.split(',')]
    elif ' ' in progression_input:
        chords = progression_input.split()
    else:
        chords = [progression_input]
    
    # Expand common patterns
    expanded_chords = []
    for chord in chords:
        if chord == '1-4-5-1':
            expanded_chords.extend(['C', 'F', 'G', 'C'])
        elif chord == '1-6-4-5':
            expanded_chords.extend(['C', 'Am', 'F', 'G'])
        elif chord == 'blues':
            expanded_chords.extend(PROGRESSIONS['blues'])
        else:
            expanded_chords.append(chord)
    
    return expanded_chords

def convert_chord_notes_to_tokens(note_sequences, stoi):
    """Convert chord notes to vocabulary tokens"""
    tokens = []
    
    print("🔍 Converting chord notes to AI tokens...")
    
    for i, note_name in enumerate(note_sequences[:16]):  # Limit initial seed
        # Try different token formats
        possible_tokens = [
            f"P{note_name}|D0.5|S0.0",
            f"P{note_name}|D0.25|S0.0",
            f"P{note_name}|D1.0|S0.0",
        ]
        
        found = False
        for token in possible_tokens:
            if token in stoi:
                tokens.append(stoi[token])
                if i < 5:  # Only show first few conversions
                    print(f"  ✅ {note_name} → {token}")
                found = True
                break
        
        if not found and i < 5:
            print(f"  ⚠️ {note_name} not found in vocabulary")
    
    print(f"✅ Converted {len(tokens)} chord notes to tokens")
    return tokens

def generate_chord_based_sequence(model, seed_tokens, length, temperature, itos):
    """Generate music sequence emphasizing chord progressions"""
    sequence = seed_tokens.copy()
    vocab_size = len(itos)
    
    for i in range(length - len(seed_tokens)):
        # Prepare input
        input_seq = sequence[-64:] if len(sequence) >= 64 else sequence
        if len(input_seq) < 64:
            input_seq = input_seq + [0] * (64 - len(input_seq))
        
        # Predict next token
        prediction = model.predict(np.array([input_seq]), verbose=0)[0]
        
        # Apply temperature
        if temperature != 1.0:
            prediction = np.log(prediction + 1e-8) / temperature
            prediction = np.exp(prediction)
        
        # Slightly bias towards chord tokens
        for token_idx, token in enumerate(itos.values()):
            if 'CHORD:' in str(token):
                prediction[token_idx] *= 1.1  # Small boost to chord probability
        
        # Normalize and sample
        prediction = prediction / np.sum(prediction)
        next_token = np.random.choice(vocab_size, p=prediction)
        sequence.append(next_token)
        
        # Progress indicator
        if (i + 1) % 30 == 0:
            progress = (i + 1) / (length - len(seed_tokens)) * 100
            print(f"  Progress: {progress:.0f}% ({i + 1}/{length - len(seed_tokens)} tokens)")
    
    return sequence

def create_chord_progression_midi(tokens, itos, chord_progression, tempo_bpm, output_file):
    """Create MIDI with enhanced chord progression structure"""
    try:
        from music21 import stream, note, chord, tempo
        
        score = stream.Stream()
        score.append(tempo.MetronomeMark(number=tempo_bpm))
        
        # Create two tracks: melody and chords
        melody_part = stream.Part()
        chord_part = stream.Part()
        
        melody_part.append(tempo.MetronomeMark(number=tempo_bpm))
        chord_part.append(tempo.MetronomeMark(number=tempo_bpm))
        
        current_time = 0
        note_count = 0
        chord_count = 0
        
        # Add the chord progression as a foundation
        chord_duration = 2.0  # Each chord lasts 2 beats
        for i, chord_name in enumerate(chord_progression):
            if chord_name in CHORD_NOTES:
                chord_notes = CHORD_NOTES[chord_name]
                c = chord.Chord(chord_notes)
                c.duration.quarterLength = chord_duration
                c.offset = i * chord_duration
                chord_part.append(c)
                chord_count += 1
        
        # Add generated melody from tokens
        melody_time = 0
        for token_idx in tokens:
            token = itos.get(token_idx, "")
            
            # Parse single notes for melody
            if token.startswith("P") and "|D" in token:
                try:
                    parts = token.split("|")
                    note_part = parts[0][1:]  # Remove 'P'
                    duration_val = float(parts[1][1:]) if len(parts) > 1 else 0.5
                    
                    n = note.Note(note_part)
                    n.duration.quarterLength = max(0.125, min(2.0, duration_val))
                    n.offset = melody_time
                    melody_part.append(n)
                    
                    melody_time += n.duration.quarterLength
                    note_count += 1
                    
                    # Limit melody length
                    if melody_time > len(chord_progression) * chord_duration:
                        break
                        
                except Exception:
                    pass
        
        # Add parts to score
        score.append(melody_part)
        score.append(chord_part)
        
        # Ensure output directory exists
        os.makedirs('outputs', exist_ok=True)
        
        # Write MIDI file
        score.write('midi', fp=f'outputs/{output_file}')
        
        print(f"🎵 Musical structure: {note_count} melody notes, {chord_count} chords")
        return True
        
    except Exception as e:
        print(f"❌ MIDI creation error: {e}")
        return False

def show_chord_usage():
    """Show usage and available chord progressions"""
    print("🎼 Advanced Chord Progression Generator")
    print("=" * 50)
    print("\nUsage:")
    print("  py -3 chord_generator.py <progression> [length] [creativity] [tempo] [output]")
    print("\n🎹 Predefined Progressions:")
    for name, chords in PROGRESSIONS.items():
        print(f"  {name:10} → {' → '.join(chords)}")
    print("\n📝 Examples:")
    print("  py -3 chord_generator.py pop")
    print("  py -3 chord_generator.py \"C Am F G\" 200 1.0")
    print("  py -3 chord_generator.py jazz 300 0.8 100 jazz_song.mid")
    print("  py -3 chord_generator.py \"Cmaj7,Am7,Dm7,G7\" 250 1.2 120")
    print("\n🎵 Chord Formats:")
    print("  Major: C, D, E, F, G, A, B")
    print("  Minor: Cm, Dm, Em, Fm, Gm, Am, Bm")
    print("  Seventh: C7, Cmaj7, Dm7, Em7, etc.")
    print("  Roman numerals: I, ii, iii, IV, V, vi, vii°")
    print("\n⚙️ Parameters:")
    print("  progression: Chord names or progression name (required)")
    print("  length: Tokens to generate (default: 250)")
    print("  creativity: 0.1-2.0 (default: 1.0)")
    print("  tempo: BPM (default: 120)")
    print("  output: Filename (default: chord_song.mid)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_chord_usage()
        sys.exit(1)
    
    # Parse arguments with better error handling
    progression_input = sys.argv[1]
    length = int(sys.argv[2]) if len(sys.argv) > 2 else 250
    creativity = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    # Handle tempo and output file more intelligently
    tempo_bpm = 120
    output_file = "chord_song.mid"
    
    # Check remaining arguments
    if len(sys.argv) > 4:
        # Try to parse as tempo first, if it fails, treat as filename
        try:
            tempo_bpm = int(sys.argv[4])
            # If tempo was provided, check for output file
            if len(sys.argv) > 5:
                output_file = sys.argv[5]
        except ValueError:
            # Fourth argument is not a number, treat as filename
            output_file = sys.argv[4]
    
    # Validate parameters
    if length < 20 or length > 1000:
        print("❌ Length must be between 20 and 1000")
        sys.exit(1)
    
    if creativity < 0.1 or creativity > 2.0:
        print("❌ Creativity must be between 0.1 and 2.0")
        sys.exit(1)
    
    if tempo_bpm < 60 or tempo_bpm > 200:
        print("❌ Tempo must be between 60 and 200 BPM")
        sys.exit(1)
    
    # Generate music
    success = generate_chord_progression_song(progression_input, length, creativity, tempo_bpm, output_file)
    sys.exit(0 if success else 1)