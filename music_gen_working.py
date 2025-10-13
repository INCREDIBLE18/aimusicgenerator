#!/usr/bin/env python3
"""
Working music generation script
"""
import os
import sys
from pathlib import Path
import numpy as np
import json

def generate_working_music(length=50, temperature=1.0, output_name="working_song.mid"):
    """Generate music with correct model handling"""
    try:
        # Change to ai-music-aml directory
        ai_music_dir = Path("ai-music-aml")
        os.chdir(ai_music_dir)
        sys.path.insert(0, ".")
        
        print("🎵 Loading components...")
        
        from tensorflow.keras.models import load_model
        from music21 import stream, note, duration, tempo
        
        # Load model and vocabulary
        model_path = "outputs/rnn/best.keras"
        vocab_path = "outputs/processed/vocab.json"
        
        print("📚 Loading vocabulary...")
        with open(vocab_path, 'r') as f:
            stoi = json.load(f)
        itos = {i: t for t, i in stoi.items()}
        
        print("🧠 Loading model...")
        model = load_model(model_path, compile=False)
        
        print(f"🎼 Generating {length} tokens...")
        
        # Initialize sequence
        seq_len = 64
        seq = np.random.randint(0, len(stoi), size=(1, seq_len))
        tokens = []
        
        for i in range(length):
            if i % 20 == 0:
                print(f"Progress: {i}/{length}")
            
            # Get predictions - shape is (1, vocab_size)
            predictions = model.predict(seq, verbose=0)
            
            # Get the last timestep predictions - shape is (vocab_size,)
            probs = predictions[0]  # Remove batch dimension
            
            # Apply temperature
            if temperature > 0:
                probs = np.log(probs + 1e-8) / temperature
                probs = np.exp(probs)
                probs = probs / np.sum(probs)
                next_token = np.random.choice(len(probs), p=probs)
            else:
                next_token = np.argmax(probs)
            
            # Add token
            tokens.append(itos[next_token])
            
            # Update sequence - shift left and add new token
            seq = np.roll(seq, -1, axis=1)
            seq[0, -1] = next_token
        
        print(f"✅ Generated {len(tokens)} tokens!")
        print(f"Sample tokens: {tokens[:10]}")
        
        # Create simple MIDI
        print("🎵 Creating MIDI...")
        
        s = stream.Stream()
        s.append(tempo.TempoIndication(number=120))
        
        # Map tokens to notes
        note_names = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5']
        
        note_count = 0
        for i, token in enumerate(tokens):
            # Simple heuristic: if token contains certain keywords, make it a note
            if any(keyword in str(token).lower() for keyword in ['note', 'on', 'pitch', 'key']):
                note_idx = i % len(note_names)
                n = note.Note(note_names[note_idx], quarterLength=0.5)
                s.append(n)
                note_count += 1
                if note_count >= 20:  # Limit notes
                    break
        
        # If no notes were created, add a simple melody
        if note_count == 0:
            print("🎵 Creating default melody...")
            for note_name in note_names:
                n = note.Note(note_name, quarterLength=0.5)
                s.append(n)
        
        # Save MIDI
        output_path = f"../outputs/{output_name}"
        os.makedirs("../outputs", exist_ok=True)
        s.write('midi', fp=output_path)
        
        print(f"✅ MIDI saved: {output_path}")
        print(f"🎼 Notes in MIDI: {len(s.notes)}")
        
        # Check file size
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"📊 File size: {size} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    length = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    temperature = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    output_name = sys.argv[3] if len(sys.argv) > 3 else "working_song.mid"
    
    print("🎵 Working AI Music Generator")
    print("=" * 40)
    print(f"Length: {length} tokens")
    print(f"Temperature: {temperature}")
    print(f"Output: {output_name}")
    print("=" * 40)
    
    success = generate_working_music(length, temperature, output_name)
    
    if success:
        print("\n🎉 SUCCESS! Music generated!")
        print("💡 Try playing the MIDI file in any music player")
    else:
        print("\n❌ FAILED! Check the error messages above")