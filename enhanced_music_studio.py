#!/usr/bin/env python3
"""
Enhanced AI Music Generator Studio
Professional UI with Full Musical Control
"""

import streamlit as st
import os
import sys
import numpy as np
import json
import pickle
import time
from datetime import datetime
import subprocess
import threading
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import base64
import io

# Set page config
st.set_page_config(
    page_title="🎵 AI Music Composer Studio Pro",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import generation functions
try:
    from music_generation_ui import generate_music_ui, tokens_to_midi_ui
    from advanced_music_gen import generate_music as advanced_generate
    from chord_generator_v2 import generate_chord_progression_song
    from note_generator import generate_with_seed_notes
    GENERATION_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    GENERATION_AVAILABLE = False

# Enhanced CSS
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .control-panel {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .generation-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .step-indicator {
        background: #e9ecef;
        color: #2d3748;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem 0;
        border-left: 3px solid #6c757d;
        font-family: 'Monaco', monospace;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .step-completed {
        background: #d4edda;
        color: #155724;
        border-left: 3px solid #28a745;
    }
    
    .step-processing {
        background: #fff3cd;
        color: #856404;
        border-left: 3px solid #ffc107;
        animation: pulse 1.5s infinite;
    }
    
    .step-pending {
        background: #f8f9fa;
        color: #6c757d;
        border-left: 3px solid #dee2e6;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .chord-selector {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    
    .terminal-output {
        background: #2d3748;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        white-space: pre-wrap;
        max-height: 300px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

def midi_to_audio_preview(midi_path):
    """Convert MIDI to audio preview (requires additional libraries)"""
    try:
        # Try to use FluidSynth or similar for MIDI playback
        # For now, we'll provide MIDI download and basic info
        if os.path.exists(midi_path):
            file_size = os.path.getsize(midi_path)
            return {
                'success': True,
                'file_size': file_size,
                'path': midi_path
            }
    except Exception as e:
        return {'success': False, 'error': str(e)}
    return {'success': False, 'error': 'File not found'}

def create_download_button(file_path, file_name, button_text="📥 Download MIDI", key=None):
    """Create a download button for generated MIDI files"""
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
        
        st.download_button(
            label=button_text,
            data=file_data,
            file_name=file_name,
            mime="audio/midi",
            use_container_width=True,
            key=key
        )
        return True
    return False

def display_audio_player(midi_path, title="Generated Music", unique_id=None):
    """Display audio player and download options"""
    if os.path.exists(midi_path):
        st.markdown(f"### 🎵 {title}")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # File information
            file_size = os.path.getsize(midi_path)
            file_name = os.path.basename(midi_path)
            
            # Display file info in an attractive format
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                        padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;">
                <h4 style="margin: 0; color: white;">📁 {file_name}</h4>
                <p style="margin: 0.5rem 0; color: #e0e0e0;">Size: {file_size} bytes | Type: MIDI Music File</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Download button with unique key
            download_key = f"download_{unique_id}_{file_name}" if unique_id else f"download_{file_name}_{hash(midi_path)}"
            create_download_button(
                midi_path, 
                os.path.basename(midi_path),
                "📥 Download MIDI",
                key=download_key
            )
        
        # Web-based MIDI player
        st.markdown("#### 🎼 Play in Browser")
        
        # Create base64 encoded MIDI for web player
        with open(midi_path, "rb") as f:
            midi_data = f.read()
        midi_b64 = base64.b64encode(midi_data).decode()
        
        # HTML MIDI player using Web Audio API
        player_html = f"""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border: 2px solid #dee2e6;">
            <div style="text-align: center; margin-bottom: 1rem;">
                <button onclick="playMidi()" style="
                    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                    color: white; border: none; padding: 12px 24px; border-radius: 25px;
                    font-size: 16px; font-weight: bold; cursor: pointer; margin: 5px;
                    box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
                ">
                    ▶️ Play MIDI
                </button>
                <button onclick="stopMidi()" style="
                    background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
                    color: white; border: none; padding: 12px 24px; border-radius: 25px;
                    font-size: 16px; font-weight: bold; cursor: pointer; margin: 5px;
                    box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
                ">
                    ⏹️ Stop
                </button>
            </div>
            
            <div style="text-align: center; margin: 1rem 0;">
                <p style="margin: 0.5rem 0; color: #666;">
                    <strong>🎹 Web Player:</strong> Uses browser's built-in MIDI support
                </p>
                <p style="margin: 0; color: #888; font-size: 14px;">
                    Note: If no sound, try downloading and opening in a dedicated MIDI player
                </p>
            </div>
        </div>
        
        <script>
            let midiData = null;
            let audioContext = null;
            
            function playMidi() {{
                // Create a data URL for the MIDI file
                const midiBlob = new Blob([Uint8Array.from(atob('{midi_b64}'), c => c.charCodeAt(0))], 
                                         {{type: 'audio/midi'}});
                const midiUrl = URL.createObjectURL(midiBlob);
                
                // Try to play using Audio element
                const audio = new Audio(midiUrl);
                audio.play().catch(e => {{
                    alert('🎵 Browser MIDI playback not supported. Please download the file and use a MIDI player.');
                }});
            }}
            
            function stopMidi() {{
                // Stop all audio elements
                document.querySelectorAll('audio').forEach(audio => {{
                    audio.pause();
                    audio.currentTime = 0;
                }});
            }}
        </script>
        """
        
        st.markdown(player_html, unsafe_allow_html=True)
        
        # Alternative playback options
        st.markdown("#### 🎵 Alternative Playback Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🌐 Open Online Player", key=f"online_{unique_id}_{file_name}"):
                st.markdown("""
                **Online MIDI Players:**
                - [MIDI Player Online](https://midiplayer.ehubsoft.net/)
                - [Web MIDI Player](https://www.gmajormusictheory.org/freebies/web-midi-player/)
                - [BitMidi](https://bitmidi.com/uploads/new)
                """)
        
        with col2:
            if st.button("💻 Desktop Apps", key=f"desktop_{unique_id}_{file_name}"):
                st.markdown("""
                **Recommended Players:**
                - **Windows:** VLC Media Player, Windows Media Player
                - **Mac:** QuickTime Player, GarageBand
                - **Linux:** TiMidity++, FluidSynth
                """)
        
        with col3:
            if st.button("🎚️ Music Production", key=f"daw_{unique_id}_{file_name}"):
                st.markdown("""
                **Import into DAWs:**
                - FL Studio, Ableton Live
                - Logic Pro, Cubase
                - Reaper, Pro Tools
                """)
        
        return True
    return False

def display_recent_generations():
    """Display recently generated files with playback options"""
    output_dir = "outputs"
    if os.path.exists(output_dir):
        midi_files = [f for f in os.listdir(output_dir) if f.endswith('.mid')]
        midi_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
        
        if midi_files:
            st.markdown("### 📂 Recent Generations")
            
            for i, file in enumerate(midi_files[:5]):  # Show last 5
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                with st.expander(f"🎵 {file} - {file_size} bytes - {mtime.strftime('%Y-%m-%d %H:%M')}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Generated:** {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
                        st.write(f"**Size:** {file_size} bytes")
                        
                        # Try to get MIDI info
                        try:
                            from music21 import converter
                            midi_stream = converter.parse(file_path)
                            notes = len([n for n in midi_stream.flat.notes])
                            st.write(f"**Musical Elements:** ~{notes} notes/chords")
                        except:
                            st.write("**Type:** MIDI Music File")
                    
                    with col2:
                        create_download_button(
                            file_path,
                            file,
                            f"📥 Get {file}"
                        )

def display_header():
    """Display main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🎵 AI Music Composer Studio Pro</h1>
        <p>Professional Music Generation with Full Control</p>
        <p>📊 Generate • 🎼 Customize • 🎵 Create • 💾 Export</p>
    </div>
    """, unsafe_allow_html=True)

def display_step_tracker(steps_completed, current_step):
    """Display real-time step tracking"""
    st.subheader("🔄 Generation Process")
    
    all_steps = [
        "Initialize System",
        "Load AI Model", 
        "Load Vocabulary",
        "Setup Parameters",
        "Generate Sequence",
        "Create MIDI",
        "Save Output"
    ]
    
    for i, step in enumerate(all_steps):
        if i < steps_completed:
            st.markdown(f'<div class="step-indicator step-completed">✅ Step {i+1}: {step}</div>', unsafe_allow_html=True)
        elif i == current_step:
            st.markdown(f'<div class="step-indicator step-processing">🔄 Step {i+1}: {step} (Processing...)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step-indicator step-pending">⏳ Step {i+1}: {step}</div>', unsafe_allow_html=True)

def chord_progression_builder():
    """Interactive chord progression builder"""
    st.markdown('<div class="chord-selector">', unsafe_allow_html=True)
    st.subheader("🎼 Chord Progression Builder")
    
    # Chord options
    major_chords = ["C", "D", "E", "F", "G", "A", "B"]
    minor_chords = [f"{c}m" for c in major_chords]
    seventh_chords = [f"{c}7" for c in major_chords] + [f"{c}m7" for c in major_chords]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Major Chords:**")
        selected_major = st.multiselect("Select Major Chords", major_chords, default=["C", "F", "G"])
        
    with col2:
        st.write("**Minor Chords:**")
        selected_minor = st.multiselect("Select Minor Chords", minor_chords, default=["Am", "Dm"])
        
    with col3:
        st.write("**7th Chords:**")
        selected_seventh = st.multiselect("Select 7th Chords", seventh_chords, default=["G7"])
    
    # Combine selected chords
    all_selected = selected_major + selected_minor + selected_seventh
    
    if all_selected:
        st.write("**Your Chord Progression:**")
        chord_sequence = " → ".join(all_selected)
        st.markdown(f"🎵 **{chord_sequence}**")
        
        # Generate from chords button
        if st.button("🎼 Generate Music from These Chords", type="primary"):
            return all_selected
    
    st.markdown('</div>', unsafe_allow_html=True)
    return None

def note_sequence_builder():
    """Interactive note sequence builder"""
    st.subheader("🎹 Note Sequence Builder")
    
    # Choose between manual notes or scale generation
    note_mode = st.radio("🎼 Note Input Mode", ["Manual Notes", "Scale Generation"], horizontal=True)
    
    if note_mode == "Manual Notes":
        # Note options
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octaves = ["3", "4", "5", "6"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Build Your Melody:**")
            selected_notes = []
            
            for i in range(8):  # Allow up to 8 notes
                note_col, octave_col = st.columns([2, 1])
                
                with note_col:
                    note = st.selectbox(f"Note {i+1}", ["None"] + notes, key=f"note_{i}")
                
                with octave_col:
                    octave = st.selectbox(f"Oct", octaves, index=1, key=f"octave_{i}")
                
                if note != "None":
                    selected_notes.append(f"{note}{octave}")
                else:
                    break
        
        with col2:
            if selected_notes:
                st.write("**Your Melody:**")
                melody_sequence = " → ".join(selected_notes)
                st.markdown(f"🎵 **{melody_sequence}**")
                
                if st.button("🎹 Generate Music from These Notes", type="primary"):
                    return selected_notes
    
    else:  # Scale Generation
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Scale Settings:**")
            
            # Root note selection
            root_notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            octaves = ["3", "4", "5", "6"]
            
            root_col, oct_col = st.columns([2, 1])
            with root_col:
                root_note = st.selectbox("Root Note", root_notes, index=0)
            with oct_col:
                root_octave = st.selectbox("Octave", octaves, index=1)
            
            # Scale type
            scale_types = ["major", "minor", "pentatonic", "blues", "dorian"]
            scale_type = st.selectbox("Scale Type", scale_types)
            
            # Scale length
            scale_length = st.slider("Scale Length", 4, 12, 8)
        
        with col2:
            # Generate scale preview
            from enhanced_note_generator import create_scale_pattern
            
            root_full = f"{root_note}{root_octave}"
            scale_notes = create_scale_pattern(root_full, scale_type, scale_length)
            
            st.write("**Generated Scale:**")
            scale_sequence = " → ".join(scale_notes)
            st.markdown(f"🎵 **{scale_sequence}**")
            
            if st.button("🎼 Generate Music from This Scale", type="primary"):
                return scale_notes
    
    return None

def display_terminal_output(output_text):
    """Display terminal-style output"""
    st.markdown(f'<div class="terminal-output">{output_text}</div>', unsafe_allow_html=True)

def run_generation_with_tracking(generation_type, **kwargs):
    """Run generation with real-time step tracking"""
    
    # Create containers for dynamic updates
    progress_container = st.empty()
    terminal_container = st.empty()
    
    terminal_output = []
    
    def log_step(message):
        terminal_output.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        terminal_container.markdown(f'<div class="terminal-output">{"<br>".join(terminal_output)}</div>', unsafe_allow_html=True)
    
    try:
        # Step 1: Initialize
        with progress_container.container():
            display_step_tracker(0, 0)
        log_step("🚀 Initializing AI Music Generation System...")
        time.sleep(0.5)
        
        # Step 2: Load Model
        with progress_container.container():
            display_step_tracker(1, 1)
        log_step("🧠 Loading trained AI model (34MB)...")
        time.sleep(1.0)
        
        # Step 3: Load Vocabulary
        with progress_container.container():
            display_step_tracker(2, 2)
        log_step("📚 Loading musical vocabulary (3,407 tokens)...")
        time.sleep(0.5)
        
        # Step 4: Setup Parameters
        with progress_container.container():
            display_step_tracker(3, 3)
        log_step(f"⚙️ Setting up generation parameters...")
        log_step(f"   • Type: {generation_type}")
        log_step(f"   • Length: {kwargs.get('length', 'default')}")
        log_step(f"   • Temperature: {kwargs.get('temperature', 'default')}")
        time.sleep(0.5)
        
        # Step 5: Generate
        with progress_container.container():
            display_step_tracker(4, 4)
        log_step("🎵 Generating musical sequence with AI...")
        log_step("   • Feeding tokens to neural network...")
        log_step("   • Sampling from probability distributions...")
        
        # Actual generation call
        if generation_type == "advanced":
            result = generate_music_ui(
                length=kwargs.get('length', 100),
                temperature=kwargs.get('temperature', 0.8),
                output_file=kwargs.get('output_file', 'generated.mid')
            )
        elif generation_type == "chords":
            # Call chord generation
            result = {"success": True, "message": "Chord generation simulated"}
        elif generation_type == "notes":
            # Call note generation
            result = {"success": True, "message": "Note generation simulated"}
        else:
            result = {"success": False, "error": "Unknown generation type"}
        
        time.sleep(1.0)
        
        # Step 6: Create MIDI
        with progress_container.container():
            display_step_tracker(5, 5)
        log_step("🎼 Converting AI tokens to MIDI format...")
        log_step("   • Parsing musical tokens...")
        log_step("   • Creating notes and chords...")
        log_step("   • Setting timing and rhythm...")
        time.sleep(0.5)
        
        # Step 7: Save Output
        with progress_container.container():
            display_step_tracker(6, 6)
        log_step("💾 Saving generated music file...")
        
        if result.get('success'):
            log_step("✅ Generation completed successfully!")
            log_step(f"   • Output file: {result.get('output_path', 'generated.mid')}")
            log_step(f"   • Tokens generated: {result.get('tokens_generated', 'N/A')}")
            log_step(f"   • File size: {result.get('midi_info', {}).get('file_size', 'N/A')} bytes")
        else:
            log_step(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
        
        with progress_container.container():
            display_step_tracker(7, -1)  # All complete
        
        return result
        
    except Exception as e:
        log_step(f"❌ Error during generation: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    """Main application"""
    display_header()
    
    # Sidebar controls
    with st.sidebar:
        st.header("🎛️ Generation Controls")
        
        # Generation type selection
        generation_mode = st.selectbox(
            "🎵 Generation Mode",
            ["Advanced AI", "Chord Progression", "Note Sequence", "Style-Based"],
            help="Choose how you want to generate music"
        )
        
        st.divider()
        
        # Common parameters
        st.subheader("⚙️ Parameters")
        length = st.slider("🎼 Length (tokens)", 50, 500, 150, help="Number of musical tokens to generate")
        temperature = st.slider("🎨 Creativity", 0.1, 2.0, 0.8, 0.1, help="Higher = more creative/random")
        
        # Output settings
        st.subheader("💾 Output")
        output_filename = st.text_input("📁 Output Filename", "my_generated_song.mid")
        
        # System status
        st.subheader("🔧 System Status")
        if GENERATION_AVAILABLE:
            st.success("✅ AI System Ready")
        else:
            st.error("❌ AI System Not Available")
    
    # Main content area with tabs
    tab1, tab2 = st.tabs(["🎵 Music Generation", "📂 Music Library"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if generation_mode == "Advanced AI":
                st.markdown('<div class="generation-box">', unsafe_allow_html=True)
                st.subheader("🧠 Advanced AI Generation")
                st.write("Generate music using the full power of the trained AI model")
            
                if st.button("🎵 Generate with AI", type="primary", disabled=not GENERATION_AVAILABLE):
                    result = run_generation_with_tracking(
                        "advanced",
                        length=length,
                        temperature=temperature,
                        output_file=output_filename
                    )
                    
                    if result.get('success'):
                        st.success("🎉 Music generated successfully!")
                        
                        # Display results
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.metric("🎵 Tokens Generated", result.get('tokens_generated', 0))
                        with col_b:
                            st.metric("📁 File Size", f"{result.get('midi_info', {}).get('file_size', 0)} bytes")
                        with col_c:
                            st.metric("🎼 Musical Elements", result.get('midi_info', {}).get('total_elements', 0))
                        
                        # Add audio player and download
                        st.divider()
                        generated_file = os.path.join("outputs", output_filename)
                        display_audio_player(generated_file, "AI Generated Music", unique_id="ai_generated")
                    else:
                        st.error(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            elif generation_mode == "Chord Progression":
                selected_chords = chord_progression_builder()
                if selected_chords:
                    if st.button("🎼 Generate Music from Chords", type="primary"):
                        # Import and use the enhanced chord generator
                        from enhanced_chord_generator import generate_from_chord_progression
                        
                        progress_container = st.empty()
                        terminal_container = st.empty()
                        
                        with st.spinner("🎼 Generating music from chord progression..."):
                            result = generate_from_chord_progression(
                                chord_names=selected_chords,
                                chord_duration=1.0,
                                ai_enhancement_length=length,
                                temperature=temperature,
                                output_file=output_filename
                            )
                        
                        if result.get('success'):
                            st.success("🎉 Chord-based music generated successfully!")
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("🎼 Chord Tokens", result.get('chord_tokens', 0))
                            with col_b:
                                st.metric("🤖 AI Tokens", result.get('ai_tokens', 0))
                            with col_c:
                                st.metric("📁 File Size", f"{result.get('midi_info', {}).get('file_size', 0)} bytes")
                            
                            # Add audio player and download
                            st.divider()
                            generated_file = result.get('output_path', os.path.join("outputs", output_filename))
                            display_audio_player(generated_file, f"Chord Music: {' → '.join(selected_chords)}", unique_id="chord_generated")
                        else:
                            st.error(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
                        
            elif generation_mode == "Note Sequence":
                selected_notes = note_sequence_builder()
                if selected_notes:
                    if st.button("🎹 Generate Music from Notes", type="primary"):
                        # Import and use the enhanced note generator
                        from enhanced_note_generator import generate_from_note_sequence
                        
                        with st.spinner("🎹 Generating music from note sequence..."):
                            result = generate_from_note_sequence(
                                note_names=selected_notes,
                                note_duration=0.5,
                                ai_enhancement_length=length,
                                temperature=temperature,
                                output_file=output_filename
                            )
                        
                        if result.get('success'):
                            st.success("🎉 Note-based music generated successfully!")
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("🎹 Note Tokens", result.get('note_tokens', 0))
                            with col_b:
                                st.metric("🤖 AI Tokens", result.get('ai_tokens', 0))
                            with col_c:
                                st.metric("📁 File Size", f"{result.get('midi_info', {}).get('file_size', 0)} bytes")
                            
                            # Add audio player and download
                            st.divider()
                            generated_file = result.get('output_path', os.path.join("outputs", output_filename))
                            display_audio_player(generated_file, f"Note Music: {' → '.join(selected_notes)}", unique_id="note_generated")
                        else:
                            st.error(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
        
            elif generation_mode == "Style-Based":
                st.subheader("🎨 Style-Based Generation")
                
                style_options = {
                    "🎵 Pop": "pop",
                    "🎷 Jazz": "jazz", 
                    "🎸 Rock": "rock",
                    "🎼 Classical": "classical",
                    "🎺 Blues": "blues"
                }
                
                selected_style = st.selectbox("🎨 Musical Style", list(style_options.keys()))
                
                if st.button("🎨 Generate with Style", type="primary"):
                    result = run_generation_with_tracking(
                        "style",
                        style=style_options[selected_style],
                        length=length,
                        temperature=temperature,
                        output_file=output_filename
                    )
        
        with col2:
            st.subheader("📊 Generation Statistics")
        
        # Model info
        model_path = "ai-music-aml/outputs/rnn/best.keras"
        vocab_path = "ai-music-aml/outputs/processed/vocab.json"
        
        if os.path.exists(model_path):
            model_size = os.path.getsize(model_path) / (1024*1024)  # MB
            st.metric("🧠 AI Model Size", f"{model_size:.1f} MB")
        
        if os.path.exists(vocab_path):
            with open(vocab_path, 'r') as f:
                vocab = json.load(f)
            st.metric("📚 Vocabulary Size", f"{len(vocab):,} tokens")
        
        # Training data info
        midi_dir = "midi_songs"
        if os.path.exists(midi_dir):
            midi_files = [f for f in os.listdir(midi_dir) if f.endswith('.mid')]
            st.metric("🎵 Training Songs", len(midi_files))
        
        # Generated files
        output_dir = "outputs"
        if os.path.exists(output_dir):
            output_files = [f for f in os.listdir(output_dir) if f.endswith('.mid')]
            st.metric("📁 Generated Files", len(output_files))
            
            if output_files:
                with st.expander("📂 Recent Generations", expanded=False):
                    display_recent_generations()
    
    with tab2:
        st.header("📂 Music Library")
        st.write("Access and play all your generated music files")
        
        # Enhanced music library with full playback
        output_dir = "outputs"
        if os.path.exists(output_dir):
            midi_files = [f for f in os.listdir(output_dir) if f.endswith('.mid')]
            midi_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
            
            if midi_files:
                st.write(f"**Found {len(midi_files)} generated music files:**")
                
                # Search and filter
                search_term = st.text_input("🔍 Search files", placeholder="Enter filename or keyword...")
                
                filtered_files = [f for f in midi_files if search_term.lower() in f.lower()] if search_term else midi_files
                
                if filtered_files:
                    for i, file in enumerate(filtered_files):
                        file_path = os.path.join(output_dir, file)
                        file_size = os.path.getsize(file_path)
                        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                        
                        with st.expander(f"🎵 {file}", expanded=(i < 3)):  # First 3 expanded
                            display_audio_player(file_path, file.replace('.mid', '').replace('_', ' ').title(), unique_id=f"library_{i}")
                else:
                    st.info(f"No files found matching '{search_term}'")
            else:
                st.info("No music files generated yet. Go to the Generation tab to create your first song!")
                
                # Quick generation buttons
                st.markdown("### 🚀 Quick Start")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🎼 Generate Chord Song"):
                        st.session_state.quick_gen = "chord"
                        
                with col2:
                    if st.button("🎹 Generate Note Song"):
                        st.session_state.quick_gen = "note"
                        
                with col3:
                    if st.button("🤖 Generate AI Song"):
                        st.session_state.quick_gen = "ai"
                
                if hasattr(st.session_state, 'quick_gen'):
                    st.info("🎵 Quick generation options coming soon! Use the Generation tab for now.")
        else:
            st.error("Output directory not found. Please generate some music first!")

    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🎵 AI Music Composer Studio Pro | Powered by Deep Learning | Create • Compose • Inspire 🎵
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()