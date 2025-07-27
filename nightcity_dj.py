#!/usr/bin/env python3
"""
Night City AI DJ
----------------
Cyberpunk-style AI DJ for DeadBeef.
Announces intros, outros, and commercials with AI TTS (Piper or ElevenLabs).

Author: Ghostroot
License: MIT
"""

import random, subprocess, os, time

# === CONFIGURATION ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

INTRO_FILE = os.path.join(CONFIG_DIR, "dj_lines.txt")
OUTRO_FILE = os.path.join(CONFIG_DIR, "dj_outros.txt")
ADS_FILE   = os.path.join(CONFIG_DIR, "dj_ads.txt")

# Piper TTS (offline)
PIPER_BIN = "piper-tts"  # Arch CLI version
MODEL_LOW  = os.path.expanduser("~/.local/share/piper/en_US-amy-low.onnx")
MODEL_HIGH = os.path.expanduser("~/.local/share/piper/en_US-amy-high.onnx")
TTS_OUTPUT = "/tmp/dj_intro.wav"

# Probabilities
INTRO_PROB = 0.9    # 90% chance to play intro
OUTRO_PROB = 0.5    # 50% chance to play outro
AD_PROB    = 0.25   # 25% chance to insert ad instead of intro

# === HELPER FUNCTIONS ===
def get_model():
    """Return best available Piper model."""
    if os.path.exists(MODEL_HIGH):
        return MODEL_HIGH
    if os.path.exists(MODEL_LOW):
        return MODEL_LOW
    print("[ERROR] No Piper model found. Please place a .onnx model in ~/.local/share/piper/")
    exit(1)

VOICE_MODEL = get_model()

def clean_name(name, fallback="Unknown"):
    """Cleans metadata, removes DeadBeef junk, extensions, and special chars."""
    name = name.strip()
    lower = name.lower()
    if not name or "deadbeef" in lower or "starting deadbeef" in lower:
        return fallback
    name = os.path.splitext(name)[0]
    for ch in ["_", "-", "|"]:
        name = name.replace(ch, " ")
    return name.title()

def get_current_track():
    """Fetch current track info with fallback to filename."""
    raw_title = subprocess.getoutput('deadbeef --nowplaying-tf "[%title%|%filename%]"')
    raw_artist = subprocess.getoutput('deadbeef --nowplaying-tf "[%artist%|Unknown Artist]"')
    return clean_name(raw_title, "Unknown Track"), clean_name(raw_artist, "Unknown Artist")

def pick_random_line(file, track="", artist=""):
    if not os.path.exists(file): return None
    with open(file) as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines: return None
    return random.choice(lines).replace("$track", track).replace("$artist", artist)

# === AUDIO PROCESSING ===
def synthesize_tts(text):
    """Generate voice using Piper TTS."""
    cmd = [PIPER_BIN, "--model", VOICE_MODEL, "--output_file", TTS_OUTPUT]
    subprocess.run(cmd, input=text.encode("utf-8"))

def apply_radio_fx():
    """Apply cyberpunk radio filter using ffmpeg."""
    fx_file = "/tmp/dj_intro_fx.wav"
    cmd = [
        "ffmpeg", "-y", "-i", TTS_OUTPUT,
        "-af", "acompressor=threshold=-15dB:ratio=4:attack=20:release=200,highpass=f=200,lowpass=f=6000,volume=2dB",
        fx_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return fx_file

def play_audio(file):
    subprocess.run(["ffplay", "-nodisp", "-autoexit", file],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# === DEADBEF CONTROL ===
def pause_deadbeef(): subprocess.run(["deadbeef", "--pause"])
def resume_deadbeef(): subprocess.run(["deadbeef", "--play"])

# === DJ SEGMENTS ===
def play_segment(line):
    if line:
        print(f"[DJ] {line}")
        synthesize_tts(line)
        processed = apply_radio_fx()
        play_audio(processed)

# === MAIN LOOP ===
def main():
    last_track = ""
    track_count = 0
    print("[INFO] Night City AI DJ is live...")

    while True:
        track, artist = get_current_track()

        if track and track != last_track:
            track_count += 1
            last_track = track

            pause_deadbeef()

            # Decide segment: Ad, Intro, or silence
            if random.random() < AD_PROB and track_count > 1:
                line = pick_random_line(ADS_FILE)
            elif random.random() < INTRO_PROB:
                line = pick_random_line(INTRO_FILE, track, artist)
            else:
                line = None

            play_segment(line)
            resume_deadbeef()

            # Optional Outro
            if random.random() < OUTRO_PROB:
                outro_line = pick_random_line(OUTRO_FILE, track, artist)
                play_segment(outro_line)

        time.sleep(5)

if __name__ == "__main__":
    main()
