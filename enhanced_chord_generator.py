#!/usr/bin/env python3
"""
Enhanced Chord-Based Music Generator
Integrates chord progressions with AI generation
"""

import os
import sys
import json
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from datetime import datetime

def chord_to_tokens(chord_name, duration=1.0, start_time=0.0):
    """Convert chord name to musical tokens"""
    
    # Chord mappings
    chord_notes = {
        # Major chords
        'C': ['C4', 'E4', 'G4'],
        'D': ['D4', 'F#4', 'A4'],
        'E': ['E4', 'G#4', 'B4'],
        'F': ['F4', 'A4', 'C5'],
        'G': ['G4', 'B4', 'D5'],
        'A': ['A4', 'C#5', 'E5'],
        'B': ['B4', 'D#5', 'F#5'],
        
        # Minor chords
        'Am': ['A4', 'C5', 'E5'],
        'Bm': ['B4', 'D5', 'F#5'],
        'Cm': ['C4', 'E-4', 'G4'],
        'Dm': ['D4', 'F4', 'A4'],
        'Em': ['E4', 'G4', 'B4'],
        'Fm': ['F4', 'A-4', 'C5'],
        'Gm': ['G4', 'B-4', 'D5'],
        
        # Seventh chords
        'C7': ['C4', 'E4', 'G4', 'B-4'],
        'D7': ['D4', 'F#4', 'A4', 'C5'],
        'E7': ['E4', 'G#4', 'B4', 'D5'],
        'F7': ['F4', 'A4', 'C5', 'E-5'],
        'G7': ['G4', 'B4', 'D5', 'F5'],
        'A7': ['A4', 'C#5', 'E5', 'G5'],
        'B7': ['B4', 'D#5', 'F#5', 'A5'],
        
        # Minor 7th chords
        'Am7': ['A4', 'C5', 'E5', 'G5'],
        'Bm7': ['B4', 'D5', 'F#5', 'A5'],
        'Cm7': ['C4', 'E-4', 'G4', 'B-4'],
        'Dm7': ['D4', 'F4', 'A4', 'C5'],
        'Em7': ['E4', 'G4', 'B4', 'D5'],
        'Fm7': ['F4', 'A-4', 'C5', 'E-5'],
        'Gm7': ['G4', 'B-4', 'D5', 'F5']
    }
    
    if chord_name not in chord_notes:
        # Default to C major if chord not found
        chord_name = 'C'
    
    notes = chord_notes[chord_name]
    notes_str = ','.join(notes)
    
    return f"CHORD:{notes_str}|D{duration}|S{start_time}"

def generate_chord_sequence(chords, chord_duration=1.0):
    """Generate a sequence of chord tokens"""
    tokens = []
    current_time = 0.0
    
    for chord in chords:
        token = chord_to_tokens(chord, chord_duration, current_time)
        tokens.append(token)
        current_time += chord_duration
    
    return tokens

def enhance_with_ai(chord_tokens, model, vocab, itos, enhancement_length=50, temperature=0.8):
    """Enhance chord progression with AI-generated content"""
    
    try:
        # Convert chord tokens to indices
        chord_indices = []
        for token in chord_tokens:
            if token in vocab:
                chord_indices.append(vocab[token])
            else:
                # If exact token not found, use a similar chord token
                chord_indices.append(0)  # Use separator token as fallback
        
        # Pad or truncate to sequence length
        sequence_length = model.input_shape[1]
        if len(chord_indices) < sequence_length:
            # Pad with random tokens
            padding_needed = sequence_length - len(chord_indices)
            padding = np.random.randint(0, len(vocab), size=padding_needed)
            seed_sequence = np.concatenate([chord_indices, padding])
        else:
            seed_sequence = np.array(chord_indices[-sequence_length:])
        
        # Generate enhanced sequence
        generated_tokens = []
        current_sequence = seed_sequence.copy()
        
        for i in range(enhancement_length):
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
        
        return chord_tokens + generated_tokens
        
    except Exception as e:
        print(f"❌ Error in AI enhancement: {e}")
        return chord_tokens

def generate_from_chord_progression(chord_names, chord_duration=1.0, ai_enhancement_length=100, temperature=0.8, output_file="chord_generated.mid"):
    """Generate music from chord progression"""
    
    print(f"🎼 Generating music from chord progression: {' → '.join(chord_names)}")
    print(f"⏰ Chord duration: {chord_duration} beats")
    print(f"🤖 AI enhancement: {ai_enhancement_length} tokens")
    print(f"🎨 Temperature: {temperature}")
    
    try:
        # Step 1: Load AI components
        print("📂 Loading AI model and vocabulary...")
        
        model_path = "ai-music-aml/outputs/rnn/best.keras"
        vocab_path = "ai-music-aml/outputs/processed/vocab.json"
        itos_path = "ai-music-aml/outputs/processed/itos.pkl"
        
        model = load_model(model_path)
        
        with open(vocab_path, 'r') as f:
            vocab = json.load(f)
        with open(itos_path, 'rb') as f:
            itos = pickle.load(f)
        
        print(f"✅ Loaded model with {len(vocab):,} vocabulary tokens")
        
        # Step 2: Generate chord tokens
        print("🎵 Converting chords to musical tokens...")
        chord_tokens = generate_chord_sequence(chord_names, chord_duration)
        
        print("🎼 Generated chord tokens:")
        for i, token in enumerate(chord_tokens):
            print(f"   {chord_names[i]}: {token}")
        
        # Step 3: Enhance with AI
        if ai_enhancement_length > 0:
            print(f"🤖 Enhancing with AI ({ai_enhancement_length} additional tokens)...")
            all_tokens = enhance_with_ai(chord_tokens, model, vocab, itos, ai_enhancement_length, temperature)
        else:
            all_tokens = chord_tokens
        
        print(f"✅ Total tokens generated: {len(all_tokens)}")
        
        # Step 4: Convert to MIDI
        print("🎵 Converting to MIDI...")
        from music_generation_ui import tokens_to_midi_ui
        
        output_path = os.path.join("outputs", output_file)
        result = tokens_to_midi_ui(all_tokens, output_path)
        
        if result['success']:
            print(f"🎉 Music generation completed successfully!")
            print(f"📁 Output file: {output_path}")
            print(f"🎵 Musical elements:")
            print(f"   • Notes: {result['notes']}")
            print(f"   • Chords: {result['chords']}")
            print(f"   • Rests: {result['rests']}")
            print(f"   • Total: {result['total_elements']}")
            print(f"📊 File size: {result['file_size']} bytes")
            
            return {
                'success': True,
                'output_path': output_path,
                'chord_tokens': len(chord_tokens),
                'ai_tokens': len(all_tokens) - len(chord_tokens),
                'total_tokens': len(all_tokens),
                'midi_info': result
            }
        else:
            print(f"❌ MIDI creation failed: {result.get('error', 'Unknown error')}")
            return {'success': False, 'error': result.get('error', 'MIDI creation failed')}
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        return {'success': False, 'error': str(e)}

def main():
    """Main function for command-line use"""
    import sys
    
    if len(sys.argv) < 2:
        print("🎼 Enhanced Chord-Based Music Generator")
        print("Usage: python enhanced_chord_generator.py <chord1> <chord2> ...")
        print("Example: python enhanced_chord_generator.py C Am F G")
        print("Example: python enhanced_chord_generator.py C Am7 F G7")
        return
    
    # Parse command line arguments
    chord_names = sys.argv[1:]
    
    # Generate music
    result = generate_from_chord_progression(
        chord_names=chord_names,
        chord_duration=1.0,
        ai_enhancement_length=100,
        temperature=0.8,
        output_file=f"chord_{'_'.join(chord_names)}.mid"
    )
    
    if result['success']:
        print(f"\n🎵 Generation successful! Play your music: {result['output_path']}")
    else:
        print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()