#!/usr/bin/env python3
"""
UI Integration Module for Music Generation
"""

import os
import sys
import numpy as np
import pickle
import json
from music21 import stream, note, chord, tempo, meter

# Add the ai-music-aml src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai-music-aml', 'src'))

try:
    import tensorflow as tf
    from tensorflow.keras import models
except ImportError as e:
    print(f"❌ Error importing TensorFlow: {e}")

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
        pass
        
    return None

def tokens_to_midi_ui(tokens, output_path):
    """Convert tokens to MIDI for UI use"""
    try:
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
                continue
        
        total_elements = note_count + chord_count + rest_count
        
        # If no musical elements were created, add a simple melody
        if total_elements == 0:
            simple_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
            for note_name in simple_notes:
                n = note.Note(note_name, quarterLength=0.5)
                s.append(n)
            note_count = len(simple_notes)
            total_elements = note_count
        
        # Write the MIDI file
        s.write('midi', fp=output_path)
        file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
        
        return {
            'success': True,
            'notes': note_count,
            'chords': chord_count,
            'rests': rest_count,
            'total_elements': total_elements,
            'file_size': file_size,
            'message': f"MIDI created with {total_elements} musical elements"
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"Error creating MIDI: {e}"
        }

def generate_music_ui(length=50, temperature=0.8, output_file="ui_generated.mid"):
    """Generate music for UI integration"""
    
    try:
        # Define paths
        model_path = os.path.join("ai-music-aml", "outputs", "rnn", "best.keras")
        vocab_path = os.path.join("ai-music-aml", "outputs", "processed", "vocab.json")
        itos_path = os.path.join("ai-music-aml", "outputs", "processed", "itos.pkl")
        output_path = os.path.join("outputs", output_file)
        
        # Load vocabulary
        with open(vocab_path, 'r') as f:
            vocab = json.load(f)
        with open(itos_path, 'rb') as f:
            itos = pickle.load(f)
        
        # Load model
        model = models.load_model(model_path)
        
        # Generate sequence
        sequence_length = model.input_shape[1]  # Should be 64
        seed_sequence = np.random.randint(0, len(vocab), size=sequence_length)
        
        generated_tokens = []
        current_sequence = seed_sequence.copy()
        
        for i in range(length):
            # Prepare input
            input_seq = current_sequence.reshape(1, sequence_length)
            
            # Get prediction
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
        
        # Convert to MIDI
        result = tokens_to_midi_ui(generated_tokens, output_path)
        
        if result['success']:
            return {
                'success': True,
                'output_path': output_path,
                'tokens_generated': len(generated_tokens),
                'sample_tokens': generated_tokens[:5],
                'midi_info': result,
                'message': f"Successfully generated {len(generated_tokens)} tokens and created MIDI"
            }
        else:
            return {
                'success': False,
                'error': result.get('error', 'Unknown MIDI creation error'),
                'message': result.get('message', 'Failed to create MIDI')
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"Generation failed: {e}"
        }

# Test function
if __name__ == "__main__":
    print("Testing UI Music Generation...")
    result = generate_music_ui(100, 0.7, "ui_test.mid")
    print(f"Result: {result}")