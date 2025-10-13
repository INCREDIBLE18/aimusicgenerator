#!/usr/bin/env python3
"""
Advanced AI Music Generator with Proper Token Parsing
"""

import sys
import os
import numpy as np
import pickle
import json
from music21 import stream, note, chord, tempo, meter, pitch, duration

# Add the ai-music-aml src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai-music-aml', 'src'))

try:
    import tensorflow as tf
    from tensorflow.keras import models
except ImportError as e:
    print(f"❌ Error importing TensorFlow: {e}")
    sys.exit(1)

def parse_token(token_str):
    """Parse a token string into musical elements"""
    try:
        if token_str.startswith('P'):  # Single note
            # Format: PD4|D0.25|S0.75
            parts = token_str.split('|')
            note_part = parts[0][1:]  # Remove 'P'
            duration_part = float(parts[1][1:]) if len(parts) > 1 else 0.5  # Remove 'D'
            
            return {
                'type': 'note',
                'pitch': note_part,
                'duration': duration_part
            }
            
        elif token_str.startswith('CHORD:'):
            # Format: CHORD:G#5,D6,E6|D0.5|S0.25
            parts = token_str.split('|')
            chord_part = parts[0][6:]  # Remove 'CHORD:'
            duration_part = float(parts[1][1:]) if len(parts) > 1 else 0.5  # Remove 'D'
            
            notes = chord_part.split(',')
            return {
                'type': 'chord',
                'notes': notes,
                'duration': duration_part
            }
            
        elif 'REST' in token_str or 'R' == token_str[0]:
            # Rest token
            duration_part = 0.5
            if '|D' in token_str:
                duration_part = float(token_str.split('|D')[1].split('|')[0])
            
            return {
                'type': 'rest',
                'duration': duration_part
            }
            
    except Exception as e:
        print(f"⚠️ Error parsing token '{token_str}': {e}")
        
    return None

def tokens_to_midi(tokens, output_path):
    """Convert tokens to MIDI with proper parsing"""
    print("🎵 Creating MIDI with advanced parsing...")
    
    # Create a music21 stream
    s = stream.Stream()
    s.append(tempo.TempoIndication(number=120))
    s.append(meter.TimeSignature(numerator=4, denominator=4))
    
    note_count = 0
    chord_count = 0
    rest_count = 0
    
    for token in tokens:
        parsed = parse_token(str(token))
        
        if parsed is None:
            continue
            
        try:
            if parsed['type'] == 'note':
                # Create a single note
                n = note.Note(parsed['pitch'], quarterLength=parsed['duration'])
                s.append(n)
                note_count += 1
                
            elif parsed['type'] == 'chord':
                # Create a chord
                chord_notes = []
                for note_name in parsed['notes']:
                    try:
                        chord_notes.append(note_name.strip())
                    except:
                        continue
                        
                if chord_notes:
                    c = chord.Chord(chord_notes, quarterLength=parsed['duration'])
                    s.append(c)
                    chord_count += 1
                    
            elif parsed['type'] == 'rest':
                # Create a rest
                r = note.Rest(quarterLength=parsed['duration'])
                s.append(r)
                rest_count += 1
                
        except Exception as e:
            print(f"⚠️ Error creating musical element: {e}")
            continue
    
    total_elements = note_count + chord_count + rest_count
    
    # If no musical elements were created, add a simple melody
    if total_elements == 0:
        print("🎵 No valid tokens found, creating default melody...")
        simple_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
        for note_name in simple_notes:
            n = note.Note(note_name, quarterLength=0.5)
            s.append(n)
        note_count = len(simple_notes)
        total_elements = note_count
    
    # Write the MIDI file
    try:
        s.write('midi', fp=output_path)
        file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
        
        print(f"✅ MIDI saved: {output_path}")
        print(f"🎼 Notes: {note_count}, Chords: {chord_count}, Rests: {rest_count}")
        print(f"📊 Total elements: {total_elements}")
        print(f"📊 File size: {file_size} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing MIDI: {e}")
        return False

def generate_music(length=50, temperature=0.8, output_file="generated_music.mid"):
    """Generate music using the trained model"""
    
    print("🎵 Advanced AI Music Generator")
    print("=" * 50)
    print(f"Length: {length} tokens")
    print(f"Temperature: {temperature}")
    print(f"Output: {output_file}")
    print("=" * 50)
    
    # Define paths
    model_path = os.path.join("ai-music-aml", "outputs", "rnn", "best.keras")
    vocab_path = os.path.join("ai-music-aml", "outputs", "processed", "vocab.json")
    itos_path = os.path.join("ai-music-aml", "outputs", "processed", "itos.pkl")
    output_path = os.path.join("outputs", output_file)
    
    print("🎵 Loading components...")
    
    # Load vocabulary
    print("📚 Loading vocabulary...")
    try:
        with open(vocab_path, 'r') as f:
            vocab = json.load(f)
        with open(itos_path, 'rb') as f:
            itos = pickle.load(f)
        print(f"📚 Vocabulary size: {len(vocab)}")
    except Exception as e:
        print(f"❌ Error loading vocabulary: {e}")
        return False
    
    # Load model
    print("🧠 Loading model...")
    try:
        model = models.load_model(model_path)
        print(f"🧠 Model loaded successfully")
        print(f"🧠 Model input shape: {model.input_shape}")
        print(f"🧠 Model output shape: {model.output_shape}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
    
    # Generate sequence
    print(f"🎼 Generating {length} tokens...")
    
    # Start with a random seed sequence
    sequence_length = model.input_shape[1]  # Should be 64
    seed_sequence = np.random.randint(0, len(vocab), size=sequence_length)
    
    generated_tokens = []
    current_sequence = seed_sequence.copy()
    
    for i in range(length):
        if i % 20 == 0:
            print(f"Progress: {i}/{length}")
        
        # Prepare input
        input_seq = current_sequence.reshape(1, sequence_length)
        
        # Get prediction
        try:
            prediction = model.predict(input_seq, verbose=0)
            
            # Apply temperature
            if temperature != 1.0:
                prediction = np.log(prediction + 1e-8) / temperature
                prediction = np.exp(prediction)
            
            # Normalize probabilities
            prediction = prediction / np.sum(prediction)
            
            # Sample next token
            next_token_idx = np.random.choice(len(prediction[0]), p=prediction[0])
            
            # Convert to token string
            if next_token_idx < len(itos):
                token_str = itos[next_token_idx]
                generated_tokens.append(token_str)
            
            # Update sequence for next iteration
            current_sequence = np.append(current_sequence[1:], next_token_idx)
            
        except Exception as e:
            print(f"❌ Error during generation step {i}: {e}")
            break
    
    print(f"✅ Generated {len(generated_tokens)} tokens!")
    if generated_tokens:
        print(f"Sample tokens: {generated_tokens[:10]}")
    
    # Convert to MIDI
    success = tokens_to_midi(generated_tokens, output_path)
    
    if success:
        print("\n🎉 SUCCESS! Music generated!")
        print("💡 Try playing the MIDI file in any music player")
        print(f"💡 File location: {output_path}")
        return True
    else:
        print("\n❌ Failed to create MIDI file")
        return False

if __name__ == "__main__":
    # Parse command line arguments
    length = 50
    temperature = 0.8
    output_file = "advanced_generated.mid"
    
    if len(sys.argv) > 1:
        try:
            length = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid length parameter")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        try:
            temperature = float(sys.argv[2])
        except ValueError:
            print("❌ Invalid temperature parameter")
            sys.exit(1)
    
    if len(sys.argv) > 3:
        output_file = sys.argv[3]
    
    # Generate music
    success = generate_music(length, temperature, output_file)
    sys.exit(0 if success else 1)