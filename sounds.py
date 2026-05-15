# sounds.py
# ── All game sounds generated with pygame synthesizer ──

import pygame
import numpy as np

# Sample rate — audio quality (standard CD quality)
SAMPLE_RATE = 44100

def make_sound(frequency, duration, volume=0.3, wave="sine", decay=True):
    """
    Generates a sound from scratch using math.
    frequency = pitch (Hz). 440 = middle A note
    duration  = length in seconds
    volume    = 0.0 to 1.0
    wave      = sine / square / noise
    decay     = fade out over time
    """
    frames = int(SAMPLE_RATE * duration)
    t      = np.linspace(0, duration, frames, False)

    # Generate the wave shape
    if wave == "sine":
        data = np.sin(2 * np.pi * frequency * t)
    elif wave == "square":
        data = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave == "noise":
        data = np.random.uniform(-1, 1, frames)

    # Apply decay (fade out)
    if decay:
        fade = np.linspace(1.0, 0.0, frames)
        data = data * fade

    # Scale to 16-bit audio range
    data = (data * volume * 32767).astype(np.int16)

    # Make stereo (2 channels)
    stereo = np.column_stack((data, data))
    sound  = pygame.sndarray.make_sound(stereo)
    return sound


def load_sounds():
    """Create and return all game sounds as a dictionary."""
    pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)

    sounds = {
        # Laser shoot — high pitch sine, short
        "shoot"     : make_sound(880,  0.12, volume=0.2, wave="sine"),

        # Explosion — low noise burst
        "explosion" : make_sound(120,  0.35, volume=0.4, wave="noise"),

        # Player hit — harsh square wave
        "hit"       : make_sound(220,  0.25, volume=0.3, wave="square"),

        # Level up — rising tone
        "levelup"   : make_sound(660,  0.4,  volume=0.25, wave="sine"),
    }
    return sounds