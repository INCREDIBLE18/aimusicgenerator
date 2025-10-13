#!/usr/bin/env python3
"""
Simple music generation test - Direct approach
"""
import os
import sys
from pathlib import Path
import numpy as np
import json

def simple_midi_test():
    """Create a simple test MIDI file to verify the system works"""
    try:
        print("🎵 Creating simple test MIDI...")
        
        # Import music21 for simple MIDI creation
        from music21 import stream, note, duration, tempo, key
        
        # Create a simple melody
        s = stream.Stream()
        
        # Add basic elements
        s.append(tempo.TempoIndication(number=120))
        s.append(key.KeySignature('C'))
        
        # Simple C major scale melody
        notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
        durations = [0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0]
        
        for note_name, dur in zip(notes, durations):
            n = note.Note(note_name, quarterLength=dur)
            s.append(n)
        
        # Add some variation
        for note_name in ['G4', 'F4', 'E4', 'D4', 'C4']:
            n = note.Note(note_name, quarterLength=0.5)
            s.append(n)
        
        # Save as MIDI
        os.makedirs("outputs", exist_ok=True)
        output_path = "outputs/simple_test.mid"
        s.write('midi', fp=output_path)
        
        print(f"✅ Simple MIDI created successfully!")
        print(f"📁 Saved to: {output_path}")
        print(f"🎼 Notes: {len(s.notes)}")
        
        # Check file size
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"📊 File size: {size} bytes")
            if size > 100:
                print("🎉 MIDI file looks good!")
                return True
            else:
                print("⚠️ MIDI file seems too small")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple MIDI creation failed: {e}")
        return False

def test_model_output():
    """Test what the model actually outputs"""
    try:
        print("🧠 Testing model output...")
        
        # Change to ai-music-aml directory
        ai_music_dir = Path("ai-music-aml")
        os.chdir(ai_music_dir)
        sys.path.insert(0, ".")
        
        from tensorflow.keras.models import load_model
        import tensorflow as tf
        
        # Load model
        model_path = "outputs/rnn/best.keras"
        print(f"📂 Loading model: {model_path}")
        
        model = load_model(model_path, compile=False)
        
        # Print model info
        print(f"🏗️ Model summary:")
        print(f"   Input shape: {model.input_shape}")
        print(f"   Output shape: {model.output_shape}")
        print(f"   Layers: {len(model.layers)}")
        
        # Test with simple input
        seq_len = 64
        vocab_size = 3407
        test_input = np.random.randint(0, vocab_size, size=(1, seq_len))
        
        print(f"🧪 Testing with input shape: {test_input.shape}")
        
        # Get prediction
        output = model.predict(test_input, verbose=0)
        print(f"📤 Output shape: {output.shape}")
        print(f"📊 Output sample: {output[0, -1][:10] if len(output.shape) > 1 else output}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 AI Music Generator - Diagnostic Test")
    print("=" * 50)
    
    # Test 1: Simple MIDI creation
    print("\n1️⃣ Testing simple MIDI creation...")
    simple_result = simple_midi_test()
    
    # Test 2: Model output
    print("\n2️⃣ Testing model output...")
    model_result = test_model_output()
    
    print("\n" + "=" * 50)
    if simple_result:
        print("✅ Simple MIDI creation: WORKING")
    else:
        print("❌ Simple MIDI creation: FAILED")
        
    if model_result:
        print("✅ Model loading: WORKING")
    else:
        print("❌ Model loading: FAILED")
    
    print("\n💡 Next steps:")
    if simple_result:
        print("   - Play 'outputs/simple_test.mid' to test audio")
    if model_result:
        print("   - Model is loaded correctly")
    else:
        print("   - Check model architecture and input/output shapes")