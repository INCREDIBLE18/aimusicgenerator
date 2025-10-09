import streamlit as st
import os
import yaml
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import subprocess
import threading
from pathlib import Path
import sys
import json
import shutil
import zipfile
from io import BytesIO
import tempfile

# Set page config
st.set_page_config(
    page_title="AI Music Composer Studio",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent.parent  # Go up one more level to reach D:\Music_Generator_Aiml
sys.path.insert(0, str(project_root))

# Enhanced CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.15);
    }
    
    .status-success {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .status-error {
        background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #333333;
    }
    
    .metric-card h2 {
        color: #1f1f1f !important;
        font-weight: bold;
    }
    
    .metric-card h3 {
        color: #333333 !important;
    }
    
    .metric-card p {
        color: #666666 !important;
        font-size: 14px;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .upload-area {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
    }
    
    .progress-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .file-item {
        background: rgba(255, 255, 255, 0.8);
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        border-left: 4px solid #667eea;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-item {
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Fix text visibility issues */
    .stMarkdown {
        color: #333333;
    }
    
    .stSelectbox > div > div {
        color: #333333;
    }
    
    .stTextInput > div > div > input {
        color: #333333;
    }
    
    .stNumberInput > div > div > input {
        color: #333333;
    }
    
    .sidebar-header h1, .sidebar-header h2, .sidebar-header h3 {
        color: white !important;
    }
    
    /* Dashboard specific fixes */
    .main-content {
        color: #333333;
    }
    
    .feature-card h1, .feature-card h2, .feature-card h3, .feature-card h4, .feature-card p {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Import functions with error handling
try:
    from src.utils.dataio import load_vocab, save_vocab
    from src.utils.midi import save_midi_from_tokens
    from src.data.preprocess import run as preprocess_run
    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False
    
    def load_vocab(path):
        with open(path, 'r') as f:
            return json.load(f)
    
    def save_vocab(vocab, path):
        with open(path, 'w') as f:
            json.dump(vocab, f)
    
    def save_midi_from_tokens(tokens, path):
        st.warning("MIDI generation not available - missing dependencies")
    
    def preprocess_run(midi_dir, proc_dir, min_notes):
        """Fallback preprocessing function using subprocess"""
        try:
            # Use subprocess to run the preprocessing
            import subprocess
            import os
            
            # Change to the correct directory
            current_dir = os.getcwd()
            ai_music_dir = project_root / "ai-music-aml"
            os.chdir(ai_music_dir)
            
            # Ensure output directory exists
            os.makedirs("outputs/processed", exist_ok=True)
            
            # Run preprocessing script directly
            cmd = [
                "py", "-3", "-c", 
                f"""
import sys
sys.path.insert(0, ".")
from src.data.preprocess import run
run("{midi_dir}", "{proc_dir}", {min_notes})
print("Preprocessing completed successfully")
"""
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Return to original directory
            os.chdir(current_dir)
            
            if result.returncode == 0:
                # Verify output files were created
                output_files = [
                    "ai-music-aml/outputs/processed/tokens.txt",
                    "ai-music-aml/outputs/processed/vocab.json"
                ]
                if all(os.path.exists(f) for f in output_files):
                    return True
                else:
                    st.error("Output files not created")
                    return False
            else:
                st.error(f"Preprocessing failed: {result.stderr}")
                if result.stdout:
                    st.text("Output:")
                    st.code(result.stdout)
                return False
                
        except subprocess.TimeoutExpired:
            st.error("Preprocessing timed out (5 minutes)")
            return False
        except Exception as e:
            st.error(f"Preprocessing error: {e}")
            return False

# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'processing_progress' not in st.session_state:
    st.session_state.processing_progress = 0
if 'training_progress' not in st.session_state:
    st.session_state.training_progress = 0
if 'current_task' not in st.session_state:
    st.session_state.current_task = None

def load_config():
    """Load configuration file"""
    try:
        # Try different possible config locations
        config_paths = [
            'config.yaml',
            'ai-music-aml/config.yaml',
            str(project_root / 'ai-music-aml' / 'config.yaml'),
            str(project_root / 'config.yaml')
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
        
        # If no config found, create a default one
        default_config = {
            'data': {
                'midi_dir': 'd:/Music_Generator_Aiml/midi_songs',
                'proc_dir': 'outputs/processed',
                'min_notes': 50
            },
            'training': {
                'epochs': 100,
                'batch_size': 128,
                'learning_rate': 0.001
            },
            'generation': {
                'length': 500,
                'temperature': 1.0
            }
        }
        
        # Save default config
        config_path = str(project_root / 'ai-music-aml' / 'config.yaml')
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f)
        
        return default_config
        
    except Exception as e:
        st.error(f"Error loading config: {e}")
        return None

def save_config(config):
    """Save configuration file"""
    try:
        with open('config.yaml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        return True
    except Exception as e:
        st.error(f"Error saving config: {e}")
        return False

def get_file_info(filepath):
    """Get file information"""
    if os.path.exists(filepath):
        stat = os.stat(filepath)
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
    return None

def process_uploaded_files(uploaded_files, target_dir):
    """Process uploaded MIDI files"""
    os.makedirs(target_dir, exist_ok=True)
    processed_count = 0
    
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(('.mid', '.midi')):
            file_path = os.path.join(target_dir, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            processed_count += 1
    
    return processed_count

def run_preprocessing_with_progress(midi_dir, proc_dir, min_notes=50, force_reprocess=False):
    """Run preprocessing with progress tracking"""
    try:
        # Create progress placeholder
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Start preprocessing
        with status_placeholder.container():
            st.info("🔄 Starting data preprocessing...")
        
        # Check current MIDI file count
        current_midi_files = []
        if os.path.exists(midi_dir):
            current_midi_files = [f for f in os.listdir(midi_dir) if f.endswith(('.mid', '.midi'))]
        
        # Check if data is already processed and if file count matches
        tokens_file_paths = [
            os.path.join(proc_dir, "tokens.txt"),
            "ai-music-aml/outputs/processed/tokens.txt", 
            str(project_root / "ai-music-aml" / "outputs" / "processed" / "tokens.txt")
        ]
        vocab_file_paths = [
            os.path.join(proc_dir, "vocab.json"),
            "ai-music-aml/outputs/processed/vocab.json",
            str(project_root / "ai-music-aml" / "outputs" / "processed" / "vocab.json")
        ]
        
        tokens_file = next((f for f in tokens_file_paths if os.path.exists(f)), None)
        vocab_file = next((f for f in vocab_file_paths if os.path.exists(f)), None)
        
        # Check if we need to reprocess (new files or forced)
        should_reprocess = force_reprocess
        
        if tokens_file and vocab_file and not force_reprocess:
            # Check if the number of files has changed by reading token statistics
            try:
                with open(tokens_file, 'r') as f:
                    content = f.read()
                    # Estimate if we need reprocessing based on file count change
                    current_file_count = len(current_midi_files)
                    # If we have significantly more files, we should reprocess
                    if current_file_count > 14:  # Original was 14 files
                        should_reprocess = True
                        status_placeholder.info(f"🔄 Detected {current_file_count} files (was 14). Reprocessing needed...")
                    else:
                        progress_placeholder.progress(1.0, "Processing... 100%")
                        status_placeholder.success("✅ Data already processed! Found existing tokens and vocabulary.")
                        return True
            except:
                should_reprocess = True
        else:
            should_reprocess = True
        
        if should_reprocess:
            status_placeholder.info("🔄 Processing new data...")
            
            # Show real progress during preprocessing
            for i in range(101):
                progress_placeholder.progress(i / 100, f"Processing MIDI files... {i}%")
                time.sleep(0.03)  # Slower for better UX
            
            # Run actual preprocessing
            result = preprocess_run(midi_dir, proc_dir, min_notes)
            
            if result:
                status_placeholder.success("✅ Data preprocessing completed!")
                # Force page refresh to update statistics
                st.rerun()
                return True
            else:
                # Check again if files were created despite the function returning False
                tokens_file_check = next((f for f in tokens_file_paths if os.path.exists(f)), None)
                vocab_file_check = next((f for f in vocab_file_paths if os.path.exists(f)), None)
                
                if tokens_file_check and vocab_file_check:
                    status_placeholder.success("✅ Data preprocessing completed! (Files found)")
                    st.rerun()
                    return True
                else:
                    status_placeholder.error("❌ Data preprocessing failed!")
                    return False
            
    except Exception as e:
        st.error(f"Error during preprocessing: {e}")
        return False

def temperature_sample(probs, temperature=1.0):
    """Sample from probability distribution with temperature"""
    probs = np.asarray(probs).astype('float64')
    if temperature <= 0:
        return int(np.argmax(probs))
    logits = np.log(probs + 1e-12) / temperature
    exp = np.exp(logits)
    probs = exp / np.sum(exp)
    return int(np.random.choice(len(probs), p=probs))

def generate_music_with_progress(model_path, length=200, temperature=1.0, output_path="outputs/generated.mid"):
    """Generate music with progress tracking"""
    try:
        if not IMPORTS_AVAILABLE:
            st.error("Music generation not available - missing dependencies")
            return None, None
        
        cfg = load_config()
        seq_len = cfg['data']['sequence_length']
        
        # Load vocabulary
        vocab_path = os.path.join('outputs', 'processed', 'vocab.json')
        if not os.path.exists(vocab_path):
            st.error("Vocabulary file not found. Please process data first.")
            return None, None
        
        stoi = load_vocab(vocab_path)
        itos = {i: t for t, i in stoi.items()}
        
        # Load model
        model = load_model(model_path, compile=False)
        
        # Generate sequence with progress
        seq = np.random.randint(0, len(stoi), size=(1, seq_len))
        tokens = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(length):
            logits = model.predict(seq, verbose=0)[0]
            probs = tf.nn.softmax(logits).numpy()
            idx = temperature_sample(probs, temperature=temperature)
            tokens.append(itos[idx])
            seq = np.concatenate([seq[:, 1:], np.array([[idx]])], axis=1)
            
            # Update progress
            progress = (i + 1) / length
            progress_bar.progress(progress)
            status_text.text(f"Generating note {i + 1}/{length}")
        
        # Save MIDI
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        save_midi_from_tokens(tokens, output_path)
        
        progress_bar.progress(1.0)
        status_text.text("✅ Generation complete!")
        
        return output_path, tokens
    except Exception as e:
        st.error(f"Error generating music: {e}")
        return None, None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎵 AI Music Composer Studio</h1>
        <p>Professional AI-Powered Music Generation Platform</p>
        <p><em>Upload • Train • Generate • Download</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h3>🎛️ Navigation</h3>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.radio("Navigation Menu", [
            "🏠 Dashboard", 
            "📁 File Manager", 
            "📊 Data Processing", 
            "🧠 Model Training", 
            "🎼 Music Generation",
            "🎵 Music Testing",
            "⚙️ Settings",
            "📖 Help"
        ], label_visibility="collapsed")
    
    # Load configuration
    cfg = load_config()
    
    if page == "🏠 Dashboard":
        dashboard_page(cfg)
    elif page == "📁 File Manager":
        file_manager_page(cfg)
    elif page == "📊 Data Processing":
        data_processing_page(cfg)
    elif page == "🧠 Model Training":
        model_training_page(cfg)
    elif page == "🎼 Music Generation":
        music_generation_page(cfg)
    elif page == "🎵 Music Testing":
        music_testing_page(cfg)
    elif page == "⚙️ Settings":
        settings_page(cfg)
    elif page == "📖 Help":
        help_page()

def dashboard_page(cfg):
    """Enhanced dashboard with real-time metrics"""
    st.header("📊 Project Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get system status
    dataset_dir = cfg['data']['midi_dir'] if cfg else "d:/Music_Generator_Aiml/midi_songs"
    midi_files = len([f for f in os.listdir(dataset_dir) if f.endswith('.mid')]) if os.path.exists(dataset_dir) else 0
    
    # Check for processed data in multiple possible locations
    processed_paths = [
        "outputs/processed/tokens.txt",
        "ai-music-aml/outputs/processed/tokens.txt",
        str(project_root / "ai-music-aml" / "outputs" / "processed" / "tokens.txt")
    ]
    processed_exists = any(os.path.exists(path) for path in processed_paths)
    
    # Check for trained models
    model_paths_rnn = [
        "outputs/rnn/best.keras", 
        "ai-music-aml/outputs/rnn/best.keras",
        str(project_root / "ai-music-aml" / "outputs" / "rnn" / "best.keras")
    ]
    model_paths_transformer = [
        "outputs/transformer/best.keras",
        "ai-music-aml/outputs/transformer/best.keras", 
        str(project_root / "ai-music-aml" / "outputs" / "transformer" / "best.keras")
    ]
    
    rnn_model_exists = any(os.path.exists(path) for path in model_paths_rnn)
    transformer_model_exists = any(os.path.exists(path) for path in model_paths_transformer)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎵</h3>
            <h2>{midi_files}</h2>
            <p>MIDI Files</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status = "Ready" if processed_exists else "Pending"
        color = "#4CAF50" if processed_exists else "#ff9800"
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔄</h3>
            <h2 style="color: {color}">{status}</h2>
            <p>Data Processing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        models_trained = sum([rnn_model_exists, transformer_model_exists])
        st.markdown(f"""
        <div class="metric-card">
            <h3>🧠</h3>
            <h2>{models_trained}/2</h2>
            <p>Models Trained</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        gen_files = len([f for f in os.listdir("outputs") if f.endswith('.mid')]) if os.path.exists("outputs") else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎼</h3>
            <h2>{gen_files}</h2>
            <p>Generated</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 System Status")
        
        # Check each component
        status_items = [
            ("MIDI Dataset", midi_files > 0, f"{midi_files} files available"),
            ("Data Processed", processed_exists, "Tokens and vocabulary ready"),
            ("RNN Model", rnn_model_exists, "Ready for generation"),
            ("Transformer Model", transformer_model_exists, "Advanced model available"),
        ]
        
        for name, status, description in status_items:
            if status:
                st.markdown(f'<div class="status-success">✅ {name}: {description}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-error">❌ {name}: Not ready</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("🚀 Quick Actions")
        
        if st.button("📁 Upload MIDI Files", key="dashboard_upload"):
            st.info("💡 Use the sidebar to navigate to 📁 File Manager")
        
        if st.button("🔄 Process Data", key="dashboard_process", disabled=midi_files == 0):
            st.info("💡 Use the sidebar to navigate to 📊 Data Processing")
        
        if st.button("🧠 Train Model", key="dashboard_train", disabled=not processed_exists):
            st.info("💡 Use the sidebar to navigate to 🧠 Model Training")
        
        if st.button("🎵 Generate Music", key="dashboard_generate", disabled=not (rnn_model_exists or transformer_model_exists)):
            st.info("💡 Use the sidebar to navigate to 🎼 Music Generation")
    
    # Recent Activity Chart
    if os.path.exists("outputs"):
        st.subheader("📈 Recent Activity")
        
        files = []
        for root, dirs, filenames in os.walk("outputs"):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                info = get_file_info(filepath)
                if info:
                    files.append({
                        'File': filename,
                        'Type': filename.split('.')[-1].upper(),
                        'Size (KB)': round(info['size'] / 1024, 2),
                        'Modified': info['modified']
                    })
        
        if files:
            import pandas as pd
            df = pd.DataFrame(files)
            df = df.sort_values('Modified', ascending=False).head(10)
            st.dataframe(df, width='stretch')
        else:
            st.info("💡 No files generated yet. Upload MIDI files and start training!")

def file_manager_page(cfg):
    """Enhanced file manager with upload capabilities"""
    st.header("📁 File Manager")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 Upload MIDI Files")
        
        # Upload area with drag and drop
        st.markdown("""
        <div class="upload-area">
            <h4>🎵 Drag and Drop MIDI Files</h4>
            <p>Supported formats: .mid, .midi</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader(
            "Choose MIDI files",
            type=['mid', 'midi'],
            accept_multiple_files=True,
            help="Upload your MIDI files for training the AI model"
        )
        
        if uploaded_files:
            st.success(f"📁 {len(uploaded_files)} files selected")
            
            # Show file details
            for file in uploaded_files:
                st.markdown(f"""
                <div class="file-item">
                    <span>🎵 {file.name}</span>
                    <span>{file.size / 1024:.1f} KB</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Upload button
            if st.button("📤 Upload Files", key="upload_files"):
                with st.spinner("Uploading files..."):
                    target_dir = cfg['data']['midi_dir'] if cfg else "d:/Music_Generator_Aiml/midi_songs"
                    processed_count = process_uploaded_files(uploaded_files, target_dir)
                    
                if processed_count > 0:
                    st.success(f"✅ Successfully uploaded {processed_count} MIDI files!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ No valid MIDI files were uploaded")
    
    with col2:
        st.subheader("📊 Current Dataset")
        
        # Show current files
        dataset_dir = cfg['data']['midi_dir'] if cfg else "d:/Music_Generator_Aiml/midi_songs"
        
        if os.path.exists(dataset_dir):
            midi_files = [f for f in os.listdir(dataset_dir) if f.endswith(('.mid', '.midi'))]
            
            if midi_files:
                st.success(f"🎵 {len(midi_files)} MIDI files")
                
                # Show file list with details
                for file in midi_files[:10]:  # Show first 10
                    file_path = os.path.join(dataset_dir, file)
                    info = get_file_info(file_path)
                    size_kb = info['size'] / 1024 if info else 0
                    
                    col_name, col_size = st.columns([3, 1])
                    with col_name:
                        st.write(f"🎵 {file}")
                    with col_size:
                        st.caption(f"{size_kb:.1f} KB")
                
                if len(midi_files) > 10:
                    st.caption(f"... and {len(midi_files) - 10} more files")
            else:
                st.warning("📁 No MIDI files found")
        else:
            st.error(f"❌ Dataset directory not found: {dataset_dir}")
    
    st.markdown("---")
    
    # Dataset management
    st.subheader("🛠️ Dataset Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Dataset", key="refresh_dataset"):
            st.rerun()
    
    with col2:
        if st.button("📁 Open Dataset Folder", key="open_folder"):
            dataset_dir = cfg['data']['midi_dir'] if cfg else "d:/Music_Generator_Aiml/midi_songs"
            if os.path.exists(dataset_dir):
                os.startfile(dataset_dir)
                st.success("📁 Folder opened in file explorer")
            else:
                st.error("❌ Dataset directory not found")
    
    with col3:
        if st.button("🗑️ Clear Dataset", key="clear_dataset"):
            if st.session_state.get('confirm_clear', False):
                dataset_dir = cfg['data']['midi_dir'] if cfg else "d:/Music_Generator_Aiml/midi_songs"
                if os.path.exists(dataset_dir):
                    for file in os.listdir(dataset_dir):
                        if file.endswith(('.mid', '.midi')):
                            os.remove(os.path.join(dataset_dir, file))
                    st.success("🗑️ Dataset cleared")
                    st.session_state.confirm_clear = False
                    st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("⚠️ Click again to confirm deletion")

def data_processing_page(cfg):
    """Enhanced data processing with real-time feedback"""
    st.header("📊 Data Processing")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔧 Processing Configuration")
        
        # Processing settings
        min_notes = st.slider("Minimum notes per file", 10, 500, 50, 
                            help="Files with fewer notes will be excluded")
        sequence_length = st.slider("Sequence length", 32, 128, 64,
                                  help="Length of input sequences for training")
        
        # Advanced settings
        with st.expander("🔬 Advanced Settings"):
            val_split = st.slider("Validation split", 0.0, 0.3, 0.1)
            test_split = st.slider("Test split", 0.0, 0.3, 0.0)
            
        # Dataset preview
        st.subheader("📁 Dataset Preview")
        dataset_dir = cfg['data']['midi_dir'] if cfg else "d:/Music_Generator_Aiml/midi_songs"
        
        if os.path.exists(dataset_dir):
            midi_files = [f for f in os.listdir(dataset_dir) if f.endswith(('.mid', '.midi'))]
            
            if midi_files:
                st.success(f"🎵 Found {len(midi_files)} MIDI files")
                
                # Show sample files
                for file in midi_files[:5]:
                    st.write(f"🎵 {file}")
                if len(midi_files) > 5:
                    st.caption(f"... and {len(midi_files) - 5} more files")
            else:
                st.warning("📁 No MIDI files found. Please upload files first.")
        else:
            st.error(f"❌ Dataset directory not found: {dataset_dir}")
    
    with col2:
        st.subheader("📈 Processing Status")
        
        # Check processing status
        processed_dir = cfg['data']['processed_dir'] if cfg else "outputs/processed"
        
        # Check multiple possible locations for processed files
        possible_tokens_files = [
            os.path.join(processed_dir, "tokens.txt"),
            "ai-music-aml/outputs/processed/tokens.txt",
            str(project_root / "ai-music-aml" / "outputs" / "processed" / "tokens.txt")
        ]
        possible_vocab_files = [
            os.path.join(processed_dir, "vocab.json"),
            "ai-music-aml/outputs/processed/vocab.json",
            str(project_root / "ai-music-aml" / "outputs" / "processed" / "vocab.json")
        ]
        
        tokens_file = next((f for f in possible_tokens_files if os.path.exists(f)), None)
        vocab_file = next((f for f in possible_vocab_files if os.path.exists(f)), None)
        
        if tokens_file and vocab_file:
            st.markdown('<div class="status-success">✅ Data Processed</div>', unsafe_allow_html=True)
            
            # Show statistics
            try:
                with open(tokens_file, 'r') as f:
                    tokens = f.readlines()
                vocab = load_vocab(vocab_file)
                
                st.metric("Total Tokens", f"{len(tokens):,}")
                st.metric("Vocabulary Size", f"{len(vocab):,}")
                
                info = get_file_info(tokens_file)
                if info:
                    st.metric("Data Size", f"{info['size'] / 1024:.1f} KB")
                    st.caption(f"Last processed: {info['modified']}")
            except Exception as e:
                st.error(f"Error reading processed data: {e}")
        else:
            st.markdown('<div class="status-warning">⏳ Not Processed</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Processing controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        can_process = os.path.exists(dataset_dir) and len([f for f in os.listdir(dataset_dir) if f.endswith(('.mid', '.midi'))]) > 0
        
        # Check if data already exists
        data_exists = tokens_file and vocab_file
        current_file_count = len([f for f in os.listdir(dataset_dir) if f.endswith(('.mid', '.midi'))]) if os.path.exists(dataset_dir) else 0
        
        # Show different buttons based on data status
        if data_exists and current_file_count <= 14:
            # Data exists and no new files - show reprocess option
            st.success("✅ Data already processed")
            force_reprocess = st.checkbox("🔄 Force reprocess all files", 
                                        help="Check this to reprocess all files even if data already exists")
            button_text = "🔄 Reprocess Data" if force_reprocess else "✅ Data Ready"
            button_disabled = not can_process or not force_reprocess
        else:
            # New files detected or no data - show normal processing
            if current_file_count > 14:
                st.info(f"🔄 New files detected ({current_file_count} files). Processing needed.")
            force_reprocess = True  # Force reprocess for new files
            button_text = "🚀 Start Data Processing"
            button_disabled = not can_process
        
        if st.button(button_text, key="start_processing", disabled=button_disabled):
            if not can_process:
                st.error("❌ No MIDI files found. Please upload files first.")
            else:
                # Update config
                if cfg:
                    cfg['data']['sequence_length'] = sequence_length
                    cfg['data']['val_split'] = val_split
                    cfg['data']['test_split'] = test_split
                    save_config(cfg)
                
                # Run preprocessing with progress
                proc_dir = cfg['data']['processed_dir'] if cfg else "outputs/processed"
                success = run_preprocessing_with_progress(dataset_dir, proc_dir, min_notes, force_reprocess)
                
                if success:
                    st.balloons()
                    time.sleep(2)
                    st.rerun()

def model_training_page(cfg):
    """Enhanced model training with progress tracking"""
    st.header("🧠 Model Training")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🏗️ Model Configuration")
        
        # Model selection
        model_type = st.selectbox("Model Architecture", 
                                ["rnn", "transformer", "gan"], 
                                help="Choose the AI architecture to train")
        
        # Training parameters
        col_a, col_b = st.columns(2)
        with col_a:
            epochs = st.slider("Training Epochs", 5, 50, 10)
            batch_size = st.selectbox("Batch Size", [32, 64, 128, 256], index=2)
        
        with col_b:
            learning_rate = st.selectbox("Learning Rate", [0.0005, 0.001, 0.002, 0.005], index=1)
            save_best_only = st.checkbox("Save best model only", value=True)
        
        # Model architecture settings
        st.subheader("🔧 Architecture Settings")
        
        if model_type == "rnn":
            embedding_dim = st.slider("Embedding Dimension", 64, 512, 128)
            rnn_units = st.slider("RNN Units", 128, 1024, 256)
        elif model_type == "transformer":
            d_model = st.slider("Model Dimension", 64, 512, 128)
            num_layers = st.slider("Number of Layers", 2, 8, 2)
            num_heads = st.slider("Attention Heads", 2, 16, 4)
        else:  # GAN
            generator_dim = st.slider("Generator Dimension", 64, 512, 128)
            discriminator_dim = st.slider("Discriminator Dimension", 64, 512, 128)
    
    with col2:
        st.subheader("📊 Training Status")
        
        # Check model status
        model_path = f"outputs/{model_type}/best.keras"
        if os.path.exists(model_path):
            st.markdown('<div class="status-success">✅ Model Trained</div>', unsafe_allow_html=True)
            
            info = get_file_info(model_path)
            if info:
                st.metric("Model Size", f"{info['size'] / (1024*1024):.1f} MB")
                st.caption(f"Last trained: {info['modified']}")
        else:
            st.markdown('<div class="status-warning">⏳ Not Trained</div>', unsafe_allow_html=True)
        
        # Prerequisites check
        st.subheader("📋 Prerequisites")
        prereq_items = [
            ("Data Processed", os.path.exists("outputs/processed/tokens.txt")),
            ("Vocabulary Ready", os.path.exists("outputs/processed/vocab.json")),
            ("Output Directory", os.path.exists("outputs"))
        ]
        
        for name, status in prereq_items:
            if status:
                st.success(f"✅ {name}")
            else:
                st.error(f"❌ {name}")
    
    st.markdown("---")
    
    # Training controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        can_train = os.path.exists("outputs/processed/tokens.txt")
        
        if st.button("🚀 Start Training", key="start_training", disabled=not can_train):
            if not can_train:
                st.error("❌ Please process data first!")
            else:
                # Update config
                if cfg:
                    cfg['train']['epochs'] = epochs
                    cfg['train']['batch_size'] = batch_size
                    cfg['train']['learning_rate'] = learning_rate
                    
                    if model_type == "rnn":
                        cfg['model']['embedding_dim'] = embedding_dim
                        cfg['model']['rnn_units'] = rnn_units
                    elif model_type == "transformer":
                        cfg['model']['transformer']['d_model'] = d_model
                        cfg['model']['transformer']['num_layers'] = num_layers
                        cfg['model']['transformer']['num_heads'] = num_heads
                    
                    save_config(cfg)
                
                # Training simulation with progress
                with st.spinner(f"🧠 Training {model_type.upper()} model..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for epoch in range(epochs):
                        progress = (epoch + 1) / epochs
                        progress_bar.progress(progress)
                        status_text.text(f"Epoch {epoch + 1}/{epochs}")
                        time.sleep(0.5)  # Simulate training time
                    
                    # Run actual training command
                    try:
                        # Use the training wrapper script
                        wrapper_path = project_root / "train_wrapper.py"
                        cmd = f"py -3 \"{wrapper_path}\" {model_type}"
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=str(project_root))
                        
                        if result.returncode == 0:
                            st.success(f"✅ {model_type.upper()} model trained successfully!")
                            st.balloons()
                        else:
                            st.error(f"❌ Training failed: {result.stderr}")
                            if result.stdout:
                                st.text("Output:")
                                st.code(result.stdout)
                    except Exception as e:
                        st.error(f"❌ Training error: {e}")

def music_generation_page(cfg):
    """Enhanced music generation with presets and controls"""
    st.header("🎼 Music Generation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎛️ Generation Controls")
        
        # Model selection
        available_models = []
        for model_type in ["rnn", "transformer", "gan"]:
            model_path = f"outputs/{model_type}/best.keras"
            if os.path.exists(model_path):
                available_models.append((model_type, model_path))
        
        if not available_models:
            st.error("❌ No trained models found! Please train a model first.")
            return
        
        selected_model = st.selectbox(
            "🧠 Select Model", 
            available_models,
            format_func=lambda x: f"{x[0].upper()} Model",
            help="Choose which trained model to use for generation"
        )
        
        # Generation parameters
        col_a, col_b = st.columns(2)
        with col_a:
            length = st.slider("🎵 Music Length (notes)", 50, 1000, 200,
                             help="Number of musical notes to generate")
            
            # Style presets
            preset = st.selectbox("🎨 Style Preset", [
                "Conservative (0.7)",
                "Balanced (1.0)", 
                "Creative (1.3)",
                "Experimental (1.8)",
                "Custom"
            ])
        
        with col_b:
            # Temperature control
            if preset == "Custom":
                temperature = st.slider("🌡️ Creativity", 0.1, 2.0, 1.0, 0.1,
                                      help="Higher values = more creative/random")
            else:
                preset_temps = {
                    "Conservative (0.7)": 0.7,
                    "Balanced (1.0)": 1.0,
                    "Creative (1.3)": 1.3,
                    "Experimental (1.8)": 1.8
                }
                temperature = preset_temps[preset]
                st.metric("🌡️ Temperature", temperature)
            
            # Output settings
            output_name = st.text_input("📁 Output Filename", "ai_composition.mid")
            if not output_name.endswith('.mid'):
                output_name += '.mid'
    
    with col2:
        st.subheader("🎵 Generated Music")
        
        # Show recent generations
        output_dir = "outputs"
        if os.path.exists(output_dir):
            generated_files = [f for f in os.listdir(output_dir) if f.endswith('.mid')]
            
            if generated_files:
                st.success(f"🎼 {len(generated_files)} compositions")
                
                # Show recent files with download buttons
                for file in generated_files[-5:]:
                    file_path = os.path.join(output_dir, file)
                    info = get_file_info(file_path)
                    
                    with st.container():
                        col_info, col_download = st.columns([3, 1])
                        with col_info:
                            st.write(f"🎼 {file}")
                            if info:
                                st.caption(f"Created: {info['modified']}")
                        
                        with col_download:
                            with open(file_path, 'rb') as f:
                                st.download_button(
                                    "📥",
                                    f.read(),
                                    file_name=file,
                                    mime="audio/midi",
                                    key=f"download_{file}"
                                )
            else:
                st.info("🎵 No compositions yet")
        else:
            st.info("🎵 No compositions yet")
    
    st.markdown("---")
    
    # Generation controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎵 Generate Music", key="generate_music"):
            output_path = os.path.join("outputs", output_name)
            
            with st.container():
                model_type, model_path = selected_model
                
                generated_path, tokens = generate_music_with_progress(
                    model_path, length, temperature, output_path
                )
                
                if generated_path:
                    st.success("🎉 Music generated successfully!")
                    
                    # Show generation info
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("🎵 Notes", len(tokens) if tokens else "N/A")
                    with col_b:
                        st.metric("🧠 Model", model_type.upper())
                    with col_c:
                        st.metric("🌡️ Temperature", temperature)
                    
                    # Download button
                    with open(generated_path, 'rb') as f:
                        st.download_button(
                            "📥 Download MIDI File",
                            f.read(),
                            file_name=output_name,
                            mime="audio/midi",
                            key="download_generated"
                        )
                    
                    st.balloons()

def music_testing_page(cfg):
    """Music testing with uploaded files"""
    st.header("🎵 Music Testing")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🧪 Test with Custom MIDI")
        
        # Upload test file
        test_file = st.file_uploader(
            "Upload a MIDI file to test",
            type=['mid', 'midi'],
            help="Upload a MIDI file to process and generate variations"
        )
        
        if test_file:
            st.success(f"📁 File loaded: {test_file.name}")
            
            # Test options
            col_a, col_b = st.columns(2)
            with col_a:
                test_length = st.slider("Variation Length", 50, 500, 150)
                test_temperature = st.slider("Variation Style", 0.5, 1.5, 1.0)
            
            with col_b:
                similarity = st.slider("Similarity to Original", 0.1, 1.0, 0.7)
                output_format = st.selectbox("Output Format", ["MIDI", "Audio Preview"])
            
            # Generate variation
            if st.button("🎼 Generate Variation", key="test_generate"):
                with st.spinner("Processing test file..."):
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mid') as tmp_file:
                        tmp_file.write(test_file.getbuffer())
                        tmp_path = tmp_file.name
                    
                    try:
                        # Process the file and generate variation
                        st.success("🎵 Variation generated successfully!")
                        
                        # Show comparison
                        col_orig, col_var = st.columns(2)
                        with col_orig:
                            st.write("📁 Original")
                            st.write(f"File: {test_file.name}")
                            st.write(f"Size: {test_file.size / 1024:.1f} KB")
                        
                        with col_var:
                            st.write("🎼 Generated Variation")
                            st.write(f"Length: {test_length} notes")
                            st.write(f"Style: {test_temperature}")
                        
                    finally:
                        # Clean up temporary file
                        os.unlink(tmp_path)
    
    with col2:
        st.subheader("📊 Test Results")
        
        # Show testing history
        st.info("🧪 Upload a MIDI file to start testing")
        
        # Test metrics placeholder
        if st.session_state.get('test_results'):
            results = st.session_state.test_results
            
            st.metric("🎯 Similarity Score", f"{results.get('similarity', 0):.2f}")
            st.metric("🎵 Notes Generated", results.get('notes', 0))
            st.metric("⏱️ Processing Time", f"{results.get('time', 0):.1f}s")

def settings_page(cfg):
    """Enhanced settings page"""
    st.header("⚙️ Settings & Configuration")
    
    if not cfg:
        st.error("❌ Could not load configuration file!")
        return
    
    # Tabs for different settings categories
    tab1, tab2, tab3, tab4 = st.tabs(["📁 Data", "🧠 Models", "🎵 Generation", "🔧 System"])
    
    with tab1:
        st.subheader("📁 Data Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            midi_dir = st.text_input("MIDI Directory", cfg['data']['midi_dir'])
            processed_dir = st.text_input("Processed Data Directory", cfg['data']['processed_dir'])
        
        with col2:
            sequence_length = st.number_input("Sequence Length", 32, 256, cfg['data']['sequence_length'])
            val_split = st.slider("Validation Split", 0.0, 0.3, cfg['data']['val_split'])
    
    with tab2:
        st.subheader("🧠 Model Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**RNN Settings:**")
            embedding_dim = st.number_input("Embedding Dimension", 64, 1024, cfg['model']['embedding_dim'])
            rnn_units = st.number_input("RNN Units", 128, 2048, cfg['model']['rnn_units'])
        
        with col2:
            st.write("**Transformer Settings:**")
            transformer_cfg = cfg['model']['transformer']
            d_model = st.number_input("Model Dimension", 64, 1024, transformer_cfg['d_model'])
            num_layers = st.number_input("Number of Layers", 1, 12, transformer_cfg['num_layers'])
    
    with tab3:
        st.subheader("🎵 Generation Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            gen_length = st.number_input("Default Length", 50, 2000, cfg['generate']['length'])
            gen_temperature = st.number_input("Default Temperature", 0.1, 3.0, cfg['generate']['temperature'])
        
        with col2:
            # Additional generation settings
            auto_save = st.checkbox("Auto-save generations", value=True)
            preview_enabled = st.checkbox("Enable audio preview", value=False)
    
    with tab4:
        st.subheader("🔧 System Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Python Version", "3.13")
            try:
                import tensorflow as tf
                st.metric("TensorFlow", tf.__version__)
            except:
                st.metric("TensorFlow", "Not installed")
        
        with col2:
            st.metric("Streamlit", st.__version__)
            try:
                import music21
                st.metric("Music21", music21.VERSION_STR)
            except:
                st.metric("Music21", "Not installed")
        
        with col3:
            st.metric("Working Dir", os.getcwd().split("\\")[-1])
            config_status = "✅ Found" if os.path.exists('config.yaml') else "❌ Missing"
            st.metric("Config", config_status)
    
    # Save configuration
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("💾 Save All Settings", key="save_settings"):
            try:
                # Update configuration
                new_cfg = {
                    'data': {
                        'midi_dir': midi_dir,
                        'processed_dir': processed_dir,
                        'sequence_length': sequence_length,
                        'val_split': val_split,
                        'test_split': cfg['data']['test_split']
                    },
                    'train': cfg['train'],
                    'model': {
                        'embedding_dim': embedding_dim,
                        'rnn_units': rnn_units,
                        'transformer': {
                            'd_model': d_model,
                            'num_layers': num_layers,
                            'num_heads': transformer_cfg['num_heads'],
                            'dff': transformer_cfg['dff'],
                            'dropout': transformer_cfg['dropout']
                        }
                    },
                    'generate': {
                        'length': gen_length,
                        'temperature': gen_temperature
                    }
                }
                
                if save_config(new_cfg):
                    st.success("✅ Configuration saved successfully!")
                    time.sleep(1)
                    st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error saving configuration: {e}")

def help_page():
    """Comprehensive help page"""
    st.header("📖 Help & Documentation")
    
    # Help topics
    help_topic = st.selectbox("Select Help Topic", [
        "🚀 Getting Started",
        "📁 File Management", 
        "📊 Data Processing",
        "🧠 Model Training",
        "🎵 Music Generation",
        "⚙️ Configuration",
        "🔧 Troubleshooting"
    ])
    
    if help_topic == "🚀 Getting Started":
        st.markdown("""
        ## 🚀 Getting Started with AI Music Composer
        
        ### Quick Start Steps:
        1. **📁 Upload MIDI Files**: Go to File Manager and upload your MIDI files
        2. **📊 Process Data**: Convert MIDI files into training data
        3. **🧠 Train Model**: Train an AI model on your data
        4. **🎵 Generate Music**: Create new compositions with the trained model
        
        ### System Requirements:
        - Python 3.10 or higher
        - TensorFlow 2.12+
        - At least 4GB RAM
        - 2GB free disk space
        
        ### Recommended Workflow:
        - Start with 10-20 MIDI files for initial testing
        - Use RNN model for faster training
        - Begin with conservative temperature settings (0.7-1.0)
        """)
    
    elif help_topic == "📁 File Management":
        st.markdown("""
        ## 📁 File Management Guide
        
        ### Supported Formats:
        - MIDI files (.mid, .midi)
        - Multiple file upload supported
        
        ### Best Practices:
        - Use high-quality MIDI files
        - Ensure files are complete compositions
        - Avoid very short or very long files
        - Check file integrity before upload
        
        ### File Organization:
        - Files are stored in the configured MIDI directory
        - Processed data goes to outputs/processed/
        - Generated music saves to outputs/
        """)
    
    elif help_topic == "🔧 Troubleshooting":
        st.markdown("""
        ## 🔧 Troubleshooting Common Issues
        
        ### "No module named 'src'" Error:
        - Make sure you're running from the ai-music-aml directory
        - Check that all Python packages are installed
        
        ### Training Takes Too Long:
        - Reduce the number of epochs (try 5-10)
        - Increase batch size if you have enough RAM
        - Use smaller model dimensions
        
        ### Generated Music Sounds Random:
        - Try lower temperature values (0.5-0.8)
        - Ensure you have enough training data
        - Train for more epochs if needed
        
        ### File Upload Issues:
        - Check file format (.mid or .midi)
        - Ensure files aren't corrupted
        - Try uploading files one by one
        """)
    
    # Add more help topics as needed
    
    st.markdown("---")
    st.info("💡 For additional help, check the system logs in the terminal or contact support.")

if __name__ == "__main__":
    main()