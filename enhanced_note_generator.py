#!/usr/bin/env python3
"""
Enhanced Note-Based Music Generator
Generate music starting from specific notes/melodies
"""

import os
import sys
import json
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from datetime import datetime

def note_to_token(note_name, duration=0.5, start_time=0.0):
    """Convert note name to musical token"""
    
    # Handle note variations
    note_name = note_name.replace('b', '-').replace('#', '#')
    
    return f"P{note_name}|D{duration}|S{start_time}"

def generate_note_sequence(notes, note_duration=0.5):
    """Generate a sequence of note tokens"""
    tokens = []
    current_time = 0.0
    
    for note in notes:
        token = note_to_token(note, note_duration, current_time)
        tokens.append(token)
        current_time += note_duration
    
    return tokens

def enhance_melody_with_ai(note_tokens, model, vocab, itos, enhancement_length=100, temperature=0.8):
    """Enhance melody with AI-generated content"""
    
    try:
        # Convert note tokens to indices
        note_indices = []
        for token in note_tokens:
            if token in vocab:
                note_indices.append(vocab[token])
            else:
                # Find similar tokens or use fallback
                note_indices.append(0)  # Use separator token as fallback
        
        # Pad or truncate to sequence length
        sequence_length = model.input_shape[1]
        if len(note_indices) < sequence_length:
            # Pad with random tokens
            padding_needed = sequence_length - len(note_indices)
            padding = np.random.randint(0, len(vocab), size=padding_needed)
            seed_sequence = np.concatenate([note_indices, padding])
        else:
            seed_sequence = np.array(note_indices[-sequence_length:])
        
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
        
        return note_tokens + generated_tokens
        
    except Exception as e:
        print(f"❌ Error in AI enhancement: {e}")
        return note_tokens

def create_scale_pattern(root_note, scale_type="major", pattern_length=8):
    """Create scale patterns for generation"""
    
    scale_patterns = {
        'major': [0, 2, 4, 5, 7, 9, 11, 12],      # Major scale
        'minor': [0, 2, 3, 5, 7, 8, 10, 12],      # Natural minor
        'pentatonic': [0, 2, 4, 7, 9, 12],        # Major pentatonic
        'blues': [0, 3, 5, 6, 7, 10, 12],         # Blues scale
        'dorian': [0, 2, 3, 5, 7, 9, 10, 12]      # Dorian mode
    }
    
    if scale_type not in scale_patterns:
        scale_type = 'major'
    
    # Note names (C-based)
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Find root note index
    root_index = 0
    for i, note in enumerate(note_names):
        if root_note.replace('4', '').replace('5', '').replace('3', '') == note:
            root_index = i
            break
    
    # Get octave
    octave = 4  # Default octave
    if '3' in root_note:
        octave = 3
    elif '5' in root_note:
        octave = 5
    elif '6' in root_note:
        octave = 6
    
    # Generate scale notes
    scale_notes = []
    pattern = scale_patterns[scale_type][:pattern_length]
    
    for interval in pattern:
        note_index = (root_index + interval) % 12
        current_octave = octave + (root_index + interval) // 12
        note_name = note_names[note_index] + str(current_octave)
        scale_notes.append(note_name)
    
    return scale_notes

def generate_from_note_sequence(note_names, note_duration=0.5, ai_enhancement_length=100, temperature=0.8, output_file="note_generated.mid"):
    """Generate music from note sequence"""
    
    print(f"🎹 Generating music from note sequence: {' → '.join(note_names)}")
    print(f"⏰ Note duration: {note_duration} beats")
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
        
        # Step 2: Generate note tokens
        print("🎵 Converting notes to musical tokens...")
        note_tokens = generate_note_sequence(note_names, note_duration)
        
        print("🎹 Generated note tokens:")
        for i, token in enumerate(note_tokens):
            print(f"   {note_names[i]}: {token}")
        
        # Step 3: Enhance with AI
        if ai_enhancement_length > 0:
            print(f"🤖 Enhancing with AI ({ai_enhancement_length} additional tokens)...")
            all_tokens = enhance_melody_with_ai(note_tokens, model, vocab, itos, ai_enhancement_length, temperature)
        else:
            all_tokens = note_tokens
        
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
                'note_tokens': len(note_tokens),
                'ai_tokens': len(all_tokens) - len(note_tokens),
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
        print("🎹 Enhanced Note-Based Music Generator")
        print("\nUsage:")
        print("  python enhanced_note_generator.py <note1> <note2> ...")
        print("  python enhanced_note_generator.py --scale <root> <type> <length>")
        print("\nExamples:")
        print("  python enhanced_note_generator.py C4 E4 G4 C5")
        print("  python enhanced_note_generator.py --scale C4 major 8")
        print("  python enhanced_note_generator.py --scale A4 minor 6")
        print("  python enhanced_note_generator.py --scale G4 pentatonic 5")
        print("\nScale types: major, minor, pentatonic, blues, dorian")
        return
    
    # Parse command line arguments
    if sys.argv[1] == '--scale':
        if len(sys.argv) < 4:
            print("❌ Scale generation requires: --scale <root> <type> [length]")
            return
        
        root_note = sys.argv[2]
        scale_type = sys.argv[3]
        pattern_length = int(sys.argv[4]) if len(sys.argv) > 4 else 8
        
        print(f"🎼 Generating {scale_type} scale from {root_note}")
        note_names = create_scale_pattern(root_note, scale_type, pattern_length)
        output_name = f"scale_{root_note}_{scale_type}.mid"
        
    else:
        # Individual notes
        note_names = sys.argv[1:]
        output_name = f"melody_{'_'.join(note_names)}.mid"
    
    # Generate music
    result = generate_from_note_sequence(
        note_names=note_names,
        note_duration=0.5,
        ai_enhancement_length=100,
        temperature=0.8,
        output_file=output_name
    )
    
    if result['success']:
        print(f"\n🎵 Generation successful! Play your music: {result['output_path']}")
    else:
        print(f"\n❌ Generation failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()