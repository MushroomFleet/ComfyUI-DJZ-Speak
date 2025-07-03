# ComfyUI-DJZ-Speak: Robotic Text-to-Speech Node

A ComfyUI custom node that brings authentic robotic text-to-speech synthesis to your workflows using eSpeak-NG formant synthesis. Based on the DJZ-Speak project, this node provides 26 distinct robotic voice presets ranging from classic computer voices to cinematic AI characters.

## Features

- **26 Robotic Voice Presets**: From classic robots to cinematic AI characters
- **Real-Time Synthesis**: Fast eSpeak-NG formant synthesis (RTF < 0.5)
- **Parameter Control**: Adjustable speed (80-300 WPM) and pitch (0-99)
- **ComfyUI Integration**: Standard AUDIO output compatible with other audio nodes
- **No Model Files**: Uses eSpeak-NG directly - no large model downloads required
- **Cross-Platform**: Windows, Linux, and macOS support

## Voice Presets

### Retro Computing
- **sbaitso**: Dr. Sbaitso (1986 retro computer TTS)
- **vintage_computer**: 1980s home computer TTS
- **dectalk**: Stephen Hawking-inspired synthesis
- **atari_sam**: Classic Atari Software Automatic Mouth
- **amiga_narrator**: Commodore Amiga computer speech
- **apple_ii**: Early Apple computer TTS

### Cinematic AI
- **hal9000**: Deep, slow computer voice (2001: A Space Odyssey)
- **c3po**: Protocol droid characteristics (Star Wars)
- **terminator**: Deep, menacing cyborg voice
- **glados**: Sarcastic AI with distinctive cadence (Portal)
- **jarvis**: Sophisticated AI assistant (Iron Man)
- **robocop**: Law enforcement android voice
- **wall_e**: Cute, expressive robot voice

### Modern & Technical
- **modern_ai**: Contemporary assistant voice
- **classic_robot**: Standard computer robot voice
- **navigation_system**: GPS/spacecraft computer voice
- **space_station**: International space communications
- **computer_alert**: Emergency system voice
- **diagnostics**: Medical/technical diagnostic voice
- **countdown**: Mission control countdown voice

### Character Voices
- **robotic_female**: Female robotic synthesis
- **robotic_child**: Higher-pitched innocent robot
- **robotic_elder**: Older, wise AI with measured speech
- **british_android**: UK-accented robotic voice
- **binary_whisper**: Quiet, mysterious data voice
- **heavy_metal**: Distorted, aggressive cyborg voice

## Installation

### Step 1: Install eSpeak-NG

**Windows:**
```bash
# Download and install from GitHub releases
# https://github.com/espeak-ng/espeak-ng/releases

# Or use Chocolatey
choco install espeak
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install espeak-ng espeak-ng-data
```

**macOS:**
```bash
brew install espeak-ng
```

### Step 2: Install ComfyUI Node

1. **Clone or download** this repository to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/
   git clone https://github.com/your-repo/ComfyUI-DJZ-Speak.git
   ```

2. **Install Python dependencies**:
   ```bash
   cd ComfyUI-DJZ-Speak
   pip install -r requirements.txt
   ```

3. **Restart ComfyUI** to load the new node.

### Step 3: Verify Installation

1. Start ComfyUI
2. Look for "DJZ-Speak TTS v1" and "DJZ-Speak TTS v2" in the "Text-to-Speech" category
3. Create a node and test with default settings

## Available Nodes

### DJZ-Speak TTS v1 (Basic)
- **Input**: Text string, voice preset, speed (80-300), pitch (0-99)
- **Output**: Audio tensor compatible with ComfyUI audio nodes
- **Features**: 26 robotic voice presets, real-time synthesis, authentic machine voices

### DJZ-Speak TTS v2 (With Effects)
- **Input**: Text string, voice preset, speed, pitch, effects toggle, effect parameters
- **Output**: Audio tensor with optional robotic effects processing
- **Features**: All v1 features plus authentic robotic effects pipeline
- **Effects**: Frequency filtering, harmonic enhancement, mechanical artifacts

## Usage

### Basic Usage (v1 Node)

1. **Add the Node**: Search for "DJZ-Speak TTS v1" in ComfyUI's node browser
2. **Enter Text**: Type your text in the text input field
3. **Select Voice**: Choose from 26 robotic voice presets
4. **Adjust Parameters**:
   - **Speed**: 80-300 WPM (words per minute)
   - **Pitch**: 0-99 (pitch level)
5. **Connect Output**: Connect the AUDIO output to other audio processing nodes

### Advanced Usage (v2 Node with Effects)

1. **Add the Node**: Search for "DJZ-Speak TTS v2" in ComfyUI's node browser
2. **Configure Basic Parameters**: Text, voice, speed, pitch (same as v1)
3. **Enable Effects**: Toggle the "effects" parameter to true
4. **Fine-tune Effects** (optional):
   - **Effect Intensity**: 0.5-2.0 (overall effect strength)
   - **Frequency Filter**: Enable/disable vintage computer filtering
   - **Harmonic Boost**: 1.0-2.0 (metallic enhancement level)
5. **Connect Output**: Enhanced robotic audio with authentic machine characteristics

### Example Workflows

**Basic Robotic Voice (v1):**
```
Text Input → DJZ-Speak TTS v1 → Audio Output
                ↓
         [Voice: "hal9000"]
         [Speed: 100]
         [Pitch: 20]
```

**Enhanced Robotic Voice (v2):**
```
Text Input → DJZ-Speak TTS v2 → Audio Output
                ↓
         [Voice: "vintage_computer"]
         [Speed: 130]
         [Pitch: 40]
         [Effects: True]
         [Intensity: 1.5]
         [Filter: True]
         [Harmonic: 1.4]
```

### Effects Processing (v2 Only)

The v2 node includes authentic robotic effects based on the original DJZ-Speak project:

**Frequency Filtering:**
- Simulates vintage computer sound by emphasizing mid-frequencies (300Hz-3kHz range)
- Creates the characteristic "tinny" sound of early computer speech
- Can be toggled on/off independently

**Harmonic Enhancement:**
- Adds metallic timbre through controlled harmonic distortion
- Creates the "mechanical" quality of robotic voices
- Adjustable from 1.0 (no enhancement) to 2.0 (strong metallic sound)

**Mechanical Artifacts:**
- Applies quantization effects to simulate digital processing limitations
- Creates subtle "digital" artifacts characteristic of vintage TTS systems
- Intensity controlled by the main effect intensity parameter

**When to Use Effects:**
- **Enable for**: Vintage computer content, retro gaming, authentic robot characters
- **Disable for**: Modern AI assistants, clean robotic speech, professional applications

### Voice Categories

**For Retro/Vintage Content:**
- `sbaitso`, `vintage_computer`, `atari_sam`, `apple_ii`

**For Sci-Fi/Cinematic:**
- `hal9000`, `terminator`, `glados`, `jarvis`

**For Friendly/Accessible:**
- `wall_e`, `robotic_child`, `modern_ai`

**For Technical/Professional:**
- `navigation_system`, `computer_alert`, `diagnostics`

**For Character/Creative:**
- `robotic_female`, `british_android`, `binary_whisper`

## Technical Details

### Audio Output Format

The node outputs standard ComfyUI AUDIO format:
```python
{
    "waveform": torch.Tensor,  # Shape: [batch, channels, samples]
    "sample_rate": 22050,      # Hz
    "path": None               # No file path (generated audio)
}
```

### Voice Parameters

Each voice preset includes:
- **eSpeak Voice**: Base voice (en, en-gb, etc.)
- **Variant**: Voice variant (m1-m4, f1-f4)
- **Default Speed**: Preset speed in WPM
- **Default Pitch**: Preset pitch level
- **Amplitude**: Volume level
- **Gap**: Word gap timing

User parameters (speed, pitch) override preset defaults.

### Performance

- **Real-Time Factor**: < 0.5 (synthesis faster than playback)
- **Memory Usage**: < 50MB during operation
- **Synthesis Latency**: < 1 second for typical phrases
- **Audio Quality**: 22kHz sample rate, mono output

## Troubleshooting

### Common Issues

1. **"eSpeak-NG not found" Error**
   - Ensure eSpeak-NG is installed and in your system PATH
   - On Windows, try adding the installation directory to PATH
   - Test with command: `espeak-ng --version`

2. **"No audio output" Error**
   - Check that the text input is not empty
   - Verify eSpeak-NG is working: `espeak-ng "test"`
   - Try a different voice preset

3. **Import Errors**
   - Install missing dependencies: `pip install -r requirements.txt`
   - Ensure ComfyUI can import torch and numpy

4. **Audio Quality Issues**
   - eSpeak-NG produces intentionally robotic audio (formant synthesis)
   - For natural speech, use other TTS nodes like KokoroTTS
   - Adjust speed and pitch parameters for better clarity

### Debug Mode

Enable debug output by checking ComfyUI console for detailed synthesis information.

## Comparison with Other TTS Nodes

### vs KokoroTTS
- **DJZ-Speak**: Robotic/mechanical voices, no model files, faster synthesis
- **KokoroTTS**: Natural human voices, requires model files, higher quality

### vs Standard TTS
- **DJZ-Speak**: Authentic retro computer sound, 26 character voices
- **Standard TTS**: Modern natural speech, limited character variety

## Development

### Adding New Voices

To add custom voice presets, modify the `voice_presets` dictionary in `DJZ_Speak_v1.py`:

```python
"custom_voice": {
    "name": "Custom Voice",
    "espeak_voice": "en",
    "speed": 140,
    "pitch": 35,
    "amplitude": 100,
    "gap": 8,
    "variant": "m3"
}
```

### eSpeak-NG Parameters

- **Voice**: Language/accent (en, en-gb, en-us, etc.)
- **Variant**: Voice character (m1-m7 for male, f1-f4 for female)
- **Speed**: Words per minute (80-300)
- **Pitch**: Pitch level (0-99)
- **Amplitude**: Volume (0-200)
- **Gap**: Word gap in 10ms units

## License

Based on DJZ-Speak project. See LICENSE file for details.

## Acknowledgments

- **DJZ-Speak Project**: Original robotic TTS implementation
- **eSpeak-NG**: Formant synthesis engine
- **ComfyUI**: Node framework and audio processing
- **Vintage Computer TTS**: Inspiration for authentic robotic characteristics

## Support

- **Issues**: Report bugs via GitHub issues
- **Documentation**: See DJZ-Speak project documentation
- **eSpeak-NG Help**: Check eSpeak-NG documentation for voice parameters

---

**ComfyUI-DJZ-Speak** - Bringing authentic robotic voices to your ComfyUI workflows.
