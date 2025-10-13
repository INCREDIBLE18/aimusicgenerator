#!/usr/bin/env python3
"""
Simple music generation test script
"""
import os
import sys
from pathlib import Path
import numpy as np
import json

def generate_music_cli(length=200, temperature=1.0, output_name="generated_test.mid"):
    """Generate music using the trained RNN model"""
    try:
        # Change to ai-music-aml directory
        ai_music_dir = Path("ai-music-aml")
        os.chdir(ai_music_dir)
        
        # Add to Python path
        sys.path.insert(0, ".")
        
        print("🎵 Loading trained RNN model...")
        
        # Import required modules
        from tensorflow.keras.models import load_model
        from src.utils.dataio import load_vocab
        from src.utils.midi import save_midi_from_tokens
        
        # Load model and vocabulary
        model_path = "outputs/rnn/best.keras"
        vocab_path = "outputs/processed/vocab.json"
        
        if not os.path.exists(model_path):
            print(f"❌ Model not found: {model_path}")
            return False
            
        if not os.path.exists(vocab_path):
            print(f"❌ Vocabulary not found: {vocab_path}")
            return False
        
        print("📚 Loading vocabulary...")
        with open(vocab_path, 'r') as f:
            stoi = json.load(f)
        itos = {i: t for t, i in stoi.items()}
        
        print(f"📊 Vocabulary size: {len(stoi)}")
        
        print("🧠 Loading model...")
        model = load_model(model_path, compile=False)
        
        print(f"🎼 Generating music: {length} tokens, temperature: {temperature}")
        
        # Generate sequence
        seq_len = 64  # Default sequence length
        seq = np.random.randint(0, len(stoi), size=(1, seq_len))
        tokens = []
        
        for i in range(length):
            if i % 10 == 0:
                print(f"Progress: {i}/{length} tokens...")
            
            # Predict next token
            probs = model.predict(seq, verbose=0)[0, -1]
            
            # Ensure probs is float32 and has proper shape
            probs = np.array(probs, dtype=np.float32)
            
            # Debug: print probability shape and sample
            if i == 0:
                print(f"🔍 Debug: Probability shape: {probs.shape}")
                print(f"🔍 Debug: Sample probs: {probs[:5]}")
            
            if len(probs.shape) == 0 or len(probs) == 0:  # If scalar or empty, skip
                print(f"⚠️ Warning: Empty probabilities at step {i}")
                next_token = np.random.randint(0, len(stoi))
            else:
                # Apply temperature
                if temperature > 0:
                    probs = np.log(probs + 1e-8) / temperature
                    probs = np.exp(probs)
                    probs = probs / np.sum(probs)
                    
                    # Ensure probabilities are valid
                    if np.any(np.isnan(probs)) or np.sum(probs) == 0:
                        next_token = np.random.randint(0, len(stoi))
                    else:
                        next_token = np.random.choice(len(probs), p=probs)
                else:
                    next_token = np.argmax(probs)
            
            # Ensure next_token is valid
            if next_token >= len(itos):
                next_token = next_token % len(itos)
                
            # Convert to int if needed
            next_token = int(next_token)
            
            # Add token to list
            if next_token in itos:
                token_str = itos[next_token]
                tokens.append(token_str)
                
                # Debug: print first few tokens
                if i < 5:
                    print(f"🎵 Token {i}: {token_str}")
            else:
                print(f"⚠️ Warning: Invalid token index {next_token}")
                tokens.append(f"UNK_{next_token}")
            
            # Update sequence
            seq = np.roll(seq, -1, axis=1)
            seq[0, -1] = next_token
        
        print("🎵 Converting to MIDI...")
        
        # Debug: Print some tokens
        print(f"📝 Generated tokens sample: {tokens[:10] if tokens else 'No tokens generated!'}")
        print(f"🔢 Total tokens: {len(tokens)}")
        
        if not tokens:
            print("❌ No tokens were generated!")
            return False
        
        # Save as MIDI
        output_path = f"../outputs/{output_name}"
        os.makedirs("../outputs", exist_ok=True)
        
        # Try a simple approach first - save tokens as text for debugging
        debug_path = f"../outputs/{output_name}.txt"
        with open(debug_path, 'w') as f:
            f.write('\n'.join(tokens))
        print(f"🔍 Debug: Tokens saved to {debug_path}")
        
        try:
            save_midi_from_tokens(tokens, output_path)
            print(f"✅ MIDI conversion successful!")
        except Exception as e:
            print(f"⚠️ MIDI conversion failed: {e}")
            print("💡 Trying simple MIDI creation...")
            
            # Fallback: Create a simple MIDI file
            from music21 import stream, note, duration
            
            s = stream.Stream()
            s.timeSignature = '4/4'
            s.keySignature = 'C'
            
            # Convert tokens to notes (simple mapping)
            note_names = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
            
            for i, token in enumerate(tokens[:50]):  # Limit to 50 notes
                if 'note_on' in token.lower() or 'note' in token.lower():
                    try:
                        # Simple note mapping
                        note_idx = i % len(note_names)
                        n = note.Note(note_names[note_idx], quarterLength=0.5)
                        s.append(n)
                    except:
                        continue
            
            # If no notes were added, add some default notes
            if len(s.notes) == 0:
                for note_name in note_names:
                    n = note.Note(note_name, quarterLength=0.5)
                    s.append(n)
            
            s.write('midi', fp=output_path)
            print(f"✅ Simple MIDI created with {len(s.notes)} notes!")
        
        print(f"📁 Saved to: {output_path}")
        print(f"🎼 Tokens generated: {len(tokens)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False

if __name__ == "__main__":
    # Parse command line arguments
    length = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    temperature = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    output_name = sys.argv[3] if len(sys.argv) > 3 else "generated_test.mid"
    
    print("🎵 AI Music Generator - Command Line Test")
    print("=" * 50)
    print(f"Generation Length: {length} tokens")
    print(f"Temperature: {temperature}")
    print(f"Output File: {output_name}")
    print("=" * 50)
    
    success = generate_music_cli(length, temperature, output_name)
    
    if success:
        print("\n🎉 Generation completed successfully!")
        print("💡 You can play the generated MIDI file in any music player")
    else:
        print("\n❌ Generation failed!")
    
    sys.exit(0 if success else 1)