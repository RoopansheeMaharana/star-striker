# highscore.py
# ── Save and load high score from a file ────────────────

import os

SCORE_FILE = "highscore.txt"

def load_high_score():
    """Read high score from file. Returns 0 if file doesn't exist."""
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0       # file was corrupted or empty
    return 0

def save_high_score(score):
    """Save score to file only if it beats the current high score."""
    current_best = load_high_score()
    if score > current_best:
        with open(SCORE_FILE, "w") as f:
            f.write(str(score))
        return True            # new high score!
    return False               # didn't beat it