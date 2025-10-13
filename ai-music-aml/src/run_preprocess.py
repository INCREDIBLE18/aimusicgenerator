import argparse
import os
import sys
import yaml

# Add current directory to path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.preprocess import run

def main(config_path, min_notes=100):
    """Run preprocessing using paths from the config file"""
    cfg = yaml.safe_load(open(config_path, 'r'))
    
    # Get paths from config
    midi_dir = cfg['data']['midi_dir']
    proc_dir = cfg['data']['processed_dir']
    
    # Ensure output directory exists
    os.makedirs(proc_dir, exist_ok=True)
    
    # Run preprocessing
    run(midi_dir, proc_dir, min_notes)
    print(f"Preprocessing completed. MIDI files from {midi_dir} processed to {proc_dir} with min_notes={min_notes}")

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='config.yaml')
    ap.add_argument('--min_notes', type=int, default=100, 
                    help='Minimum number of notes required in a MIDI file to include it')
    args = ap.parse_args()
    main(args.config, args.min_notes)