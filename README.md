# 🎧 Night City AI DJ

A cyberpunk-style **AI radio DJ** that injects immersive DJ chatter, ads, and outros into your local music playback.  
Runs on **Linux + DeadBeef** with **Piper TTS** (offline) or **ElevenLabs** (cloud).

---

## ✨ Features
- 🎛️ Randomized intros, outros, and commercials
- 🔊 Radio FX processing for gritty cyberpunk sound
- 🎶 Automatically detects current track/artist
- 🐍 Written in Python, fully configurable
- 🛠️ Works offline with Piper TTS

---

## 🛠️ Installation

### 1. Prerequisites

Install DeadBeef:
```bash
sudo pacman -S deadbeef
sudo pacman -S ffmpeg python
```
---

#### (Optional) install yay for AUR packages
```
sudo pacman -S git base-devel
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si
```
---

#### Install Piper TTS
```
yay -S piper-tts
```
#### Create the Piper folder
```
mkdir -p ~/.local/share/piper
```

#### Clone the project
```
git clone https://github.com/RobinV87/nightcity_AI_DJ.git
cd nightcity-ai-dj
pip install -r requirements.txt
```
---

#### Install Python dependencies
```
pip install -r requirements.txt
```
#### Customize the DJ chatter:

    config/dj_lines.txt → DJ intros

    config/dj_outros.txt → DJ outros

    config/dj_ads.txt → Cyberpunk ads

You can freely edit these text files.

---

#### Testing:
```
echo "Night City is alive." | piper-tts --model ~/.local/share/piper/en_US-amy-high.onnx --output_file test.wav
ffplay -nodisp -autoexit test.wav
```
---

## Usage

▶️ Usage

    Start DeadBeef and play music.

    Run the AI DJ in another terminal:
```
python3 nightcity_dj.py
```

You’ll hear:

    DJ intros/outros between songs

    Commercials at random intervals

    Radio-style audio effects

## 🎨 Customization

    ✏️ Add more DJ lines by editing text files in config/

    🎛️ Enable Glitch FX by placing a glitch.wav in sfx/ and adding FFmpeg overlay

    🗣️ Switch Voices by downloading different Piper models from HuggingFace

    🌐 ElevenLabs Support: Add your API key and modify the TTS function for cloud-based ultra-realistic voices (future-ready in script)

#### ⚡ Auto-Start (Optional)

Add to your startup:
```
echo "~/nightcity-ai-dj/nightcity_dj.py &" >> ~/.xprofile
```


