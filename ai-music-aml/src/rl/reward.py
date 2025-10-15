"""Simple reward functions and a REINFORCE-style fine-tune skeleton.
This keeps things compact; for serious RL you may integrate stable-baselines.
"""
import numpy as np

SCALE = set(['C', 'D', 'E', 'F', 'G', 'A', 'B'])

def in_scale(pitch_token: str) -> float:
    # pitch_token like 'PC4' or 'PFS#4' etc; we check first char after 'P'
    try:
        if pitch_token.startswith('P'):
            p = pitch_token[1:]
        elif pitch_token.startswith('CHORD:'):
            # reward avg over chord notes
            notes = pitch_token.split(':',1)[1].split(',')
            return float(np.mean([in_scale('P'+n) for n in notes]))
        else:
            p = pitch_token
        letter = p[0].upper()
        return 1.0 if letter in SCALE else 0.5
    except Exception:
        return 0.2

def rhythm_stability(duration_token: str, step_token: str) -> float:
    # encourage quarter/half notes and steady steps
    score = 0.0
    try:
        d = float(duration_token[1:]) if duration_token.startswith('D') else float(duration_token)
        s = float(step_token[1:]) if step_token.startswith('S') else float(step_token)
        if d in (0.25, 0.5, 1.0, 2.0): score += 0.5
        if s in (0.25, 0.5, 1.0): score += 0.5
        return score
    except Exception:
        return 0.2
