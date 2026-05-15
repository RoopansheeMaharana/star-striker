# sounds.py
import pygame
import numpy as np
import io

SAMPLE_RATE = 44100

def make_sound(frequency, duration, volume=0.3, wave="sine", decay=True):
    frames = int(SAMPLE_RATE * duration)
    t      = np.linspace(0, duration, frames, False)

    if wave == "sine":
        data = np.sin(2 * np.pi * frequency * t)
    elif wave == "square":
        data = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave == "noise":
        data = np.random.uniform(-1, 1, frames)
    else:
        data = np.sin(2 * np.pi * frequency * t)

    if decay:
        fade = np.linspace(1.0, 0.0, frames)
        data = data * fade

    # Scale to 16-bit
    data = (data * volume * 32767).astype(np.int16)

    # Duplicate to stereo
    stereo = np.repeat(data.reshape(-1, 1), 2, axis=1)
    stereo = np.ascontiguousarray(stereo, dtype=np.int16)

    # Write as WAV into memory and load it
    import wave, struct
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(stereo.tobytes())
    buf.seek(0)
    return pygame.mixer.Sound(buf)


def load_sounds():
    pygame.mixer.quit()
    pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)

    sounds = {
        "shoot"     : make_sound(880,  0.12, volume=0.2, wave="sine"),
        "explosion" : make_sound(120,  0.35, volume=0.4, wave="noise"),
        "hit"       : make_sound(220,  0.25, volume=0.3, wave="square"),
        "levelup"   : make_sound(660,  0.4,  volume=0.25, wave="sine"),
    }
    return sounds
