#!/usr/bin/env python
import os
import torch
import numpy as np
import subprocess
import tempfile
import logging
from pathlib import Path
from typing import Dict, Any, Optional


class DJZSpeak_v1:
    def __init__(self):
        self.type = "DJZSpeak_v1"
        self.output_type = "AUDIO"
        self.output_dims = 1
        self.compatible_decorators = []
        self.required_extensions = []
        self.category = "Text-to-Speech"
        self.name = "DJZ-Speak TTS Processor"
        self.description = "Robotic text-to-speech using eSpeak-NG formant synthesis with authentic machine voices."
        
        # Hardcoded voices list from DJZ-Speak default_voices.json
        self.voices = [
            "classic_robot", "dectalk", "sbaitso", "hal9000", "c3po",
            "vintage_computer", "modern_ai", "robotic_female", "terminator",
            "glados", "jarvis", "robocop", "wall_e", "computer_alert",
            "navigation_system", "diagnostics", "countdown", "atari_sam",
            "amiga_narrator", "apple_ii", "robotic_child", "robotic_elder",
            "binary_whisper", "heavy_metal", "british_android", "space_station"
        ]
        
        # Voice configurations hardcoded from DJZ-Speak
        self.voice_presets = {
            "classic_robot": {
                "name": "Classic Robot",
                "espeak_voice": "en",
                "speed": 140,
                "pitch": 35,
                "amplitude": 100,
                "gap": 8,
                "variant": "m3"
            },
            "dectalk": {
                "name": "DECtalk Style",
                "espeak_voice": "en",
                "speed": 120,
                "pitch": 25,
                "amplitude": 95,
                "gap": 10,
                "variant": "m1"
            },
            "sbaitso": {
                "name": "Dr. Sbaitso",
                "espeak_voice": "en",
                "speed": 160,
                "pitch": 45,
                "amplitude": 110,
                "gap": 6,
                "variant": "m2"
            },
            "hal9000": {
                "name": "HAL 9000",
                "espeak_voice": "en",
                "speed": 100,
                "pitch": 20,
                "amplitude": 85,
                "gap": 15,
                "variant": "m1"
            },
            "c3po": {
                "name": "C-3PO Style",
                "espeak_voice": "en",
                "speed": 150,
                "pitch": 55,
                "amplitude": 105,
                "gap": 5,
                "variant": "m4"
            },
            "vintage_computer": {
                "name": "Vintage Computer",
                "espeak_voice": "en",
                "speed": 130,
                "pitch": 40,
                "amplitude": 100,
                "gap": 12,
                "variant": "m3"
            },
            "modern_ai": {
                "name": "Modern AI",
                "espeak_voice": "en",
                "speed": 160,
                "pitch": 42,
                "amplitude": 95,
                "gap": 4,
                "variant": "m2"
            },
            "robotic_female": {
                "name": "Robotic Female",
                "espeak_voice": "en",
                "speed": 145,
                "pitch": 65,
                "amplitude": 100,
                "gap": 7,
                "variant": "f3"
            },
            "terminator": {
                "name": "Terminator",
                "espeak_voice": "en",
                "speed": 110,
                "pitch": 18,
                "amplitude": 90,
                "gap": 12,
                "variant": "m1"
            },
            "glados": {
                "name": "GLaDOS",
                "espeak_voice": "en",
                "speed": 135,
                "pitch": 50,
                "amplitude": 95,
                "gap": 8,
                "variant": "f2"
            },
            "jarvis": {
                "name": "JARVIS",
                "espeak_voice": "en",
                "speed": 155,
                "pitch": 38,
                "amplitude": 100,
                "gap": 4,
                "variant": "m2"
            },
            "robocop": {
                "name": "RoboCop",
                "espeak_voice": "en",
                "speed": 125,
                "pitch": 30,
                "amplitude": 105,
                "gap": 10,
                "variant": "m3"
            },
            "wall_e": {
                "name": "WALL-E",
                "espeak_voice": "en",
                "speed": 140,
                "pitch": 60,
                "amplitude": 110,
                "gap": 6,
                "variant": "m4"
            },
            "computer_alert": {
                "name": "Computer Alert",
                "espeak_voice": "en",
                "speed": 170,
                "pitch": 45,
                "amplitude": 115,
                "gap": 3,
                "variant": "f1"
            },
            "navigation_system": {
                "name": "Navigation System",
                "espeak_voice": "en",
                "speed": 150,
                "pitch": 42,
                "amplitude": 100,
                "gap": 5,
                "variant": "f2"
            },
            "diagnostics": {
                "name": "Medical Scanner",
                "espeak_voice": "en",
                "speed": 130,
                "pitch": 40,
                "amplitude": 95,
                "gap": 7,
                "variant": "m2"
            },
            "countdown": {
                "name": "Mission Control",
                "espeak_voice": "en",
                "speed": 120,
                "pitch": 35,
                "amplitude": 105,
                "gap": 15,
                "variant": "m1"
            },
            "atari_sam": {
                "name": "Atari SAM",
                "espeak_voice": "en",
                "speed": 140,
                "pitch": 50,
                "amplitude": 110,
                "gap": 8,
                "variant": "m3"
            },
            "amiga_narrator": {
                "name": "Amiga Narrator",
                "espeak_voice": "en",
                "speed": 135,
                "pitch": 48,
                "amplitude": 105,
                "gap": 9,
                "variant": "m2"
            },
            "apple_ii": {
                "name": "Apple II",
                "espeak_voice": "en",
                "speed": 125,
                "pitch": 45,
                "amplitude": 100,
                "gap": 12,
                "variant": "m3"
            },
            "robotic_child": {
                "name": "Robotic Child",
                "espeak_voice": "en",
                "speed": 160,
                "pitch": 75,
                "amplitude": 105,
                "gap": 5,
                "variant": "f4"
            },
            "robotic_elder": {
                "name": "Robotic Elder",
                "espeak_voice": "en",
                "speed": 105,
                "pitch": 28,
                "amplitude": 90,
                "gap": 18,
                "variant": "m1"
            },
            "binary_whisper": {
                "name": "Binary Whisper",
                "espeak_voice": "en",
                "speed": 180,
                "pitch": 55,
                "amplitude": 70,
                "gap": 3,
                "variant": "f3"
            },
            "heavy_metal": {
                "name": "Heavy Metal",
                "espeak_voice": "en",
                "speed": 145,
                "pitch": 22,
                "amplitude": 120,
                "gap": 6,
                "variant": "m1"
            },
            "british_android": {
                "name": "British Android",
                "espeak_voice": "en-gb",
                "speed": 145,
                "pitch": 40,
                "amplitude": 100,
                "gap": 6,
                "variant": "m3"
            },
            "space_station": {
                "name": "Space Station",
                "espeak_voice": "en",
                "speed": 140,
                "pitch": 38,
                "amplitude": 95,
                "gap": 8,
                "variant": "m2"
            }
        }
        
        # Find eSpeak-NG executable
        self.espeak_path = self._find_espeak_executable()
        if not self.espeak_path:
            print("WARNING: eSpeak-NG not found. Please install eSpeak-NG for DJZ-Speak to work.")

    def _find_espeak_executable(self) -> Optional[str]:
        """Find eSpeak-NG executable."""
        import shutil
        
        # Common executable names
        executable_names = ['espeak-ng', 'espeak']
        
        # Check if in PATH
        for name in executable_names:
            path = shutil.which(name)
            if path:
                return path
        
        # Check common installation paths
        common_paths = [
            '/usr/bin/espeak-ng',
            '/usr/local/bin/espeak-ng',
            '/opt/espeak-ng/bin/espeak-ng',
            'C:\\Program Files\\eSpeak NG\\espeak-ng.exe',
            'C:\\Program Files (x86)\\eSpeak NG\\espeak-ng.exe',
        ]
        
        for path in common_paths:
            if Path(path).exists():
                return path
        
        return None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Hello, I am a robot"}),
                "voice": (["classic_robot", "dectalk", "sbaitso", "hal9000", "c3po",
                          "vintage_computer", "modern_ai", "robotic_female", "terminator",
                          "glados", "jarvis", "robocop", "wall_e", "computer_alert",
                          "navigation_system", "diagnostics", "countdown", "atari_sam",
                          "amiga_narrator", "apple_ii", "robotic_child", "robotic_elder",
                          "binary_whisper", "heavy_metal", "british_android", "space_station"],),
                "speed": ("INT", {"default": 140, "min": 80, "max": 300, "step": 1}),
                "pitch": ("INT", {"default": 35, "min": 0, "max": 99, "step": 1})
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "synthesize"

    def synthesize(self, text, voice, speed, pitch):
        print(f"DJZ-Speak synthesizing: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"Using voice: {voice} at speed: {speed}, pitch: {pitch}")
        
        if not self.espeak_path:
            raise ValueError("eSpeak-NG not found. Please install eSpeak-NG to use DJZ-Speak.")
        
        if not text or not text.strip():
            raise ValueError("Empty text provided for synthesis")
        
        # Get voice configuration
        voice_config = self.voice_presets.get(voice, self.voice_presets["classic_robot"])
        
        # Override speed and pitch with user parameters
        actual_speed = speed
        actual_pitch = pitch
        
        try:
            # Build eSpeak-NG command
            cmd = [
                self.espeak_path,
                '-v', f"{voice_config['espeak_voice']}+{voice_config['variant']}",
                '-s', str(actual_speed),
                '-p', str(actual_pitch),
                '-a', str(voice_config['amplitude']),
                '-g', str(voice_config['gap']),
                '--stdout'
            ]
            
            # Add text as argument
            cmd.append(text.strip())
            
            # Execute eSpeak-NG
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=30,
                check=True
            )
            
            if not result.stdout:
                raise ValueError("eSpeak-NG produced no audio output")
            
            # Convert WAV bytes to numpy array
            audio_data = self._wav_bytes_to_numpy(result.stdout)
            
            # Convert to torch tensor with ComfyUI format
            if audio_data.ndim == 1:
                # Mono audio - add batch and channel dimensions
                audio_tensor = torch.from_numpy(audio_data).float().unsqueeze(0).unsqueeze(0)
            else:
                # Stereo audio - add batch dimension
                audio_tensor = torch.from_numpy(audio_data).float().unsqueeze(0)
            
            # Sample rate from eSpeak-NG (typically 22050)
            sample_rate = 22050
            
            result = {
                "waveform": audio_tensor.contiguous().detach(),
                "sample_rate": sample_rate,
                "path": None
            }
            
            print("DJZ-Speak synthesis complete.")
            return (result,)
            
        except subprocess.TimeoutExpired:
            raise ValueError("eSpeak-NG synthesis timed out")
        except subprocess.CalledProcessError as e:
            error_msg = f"eSpeak-NG process failed: {e}"
            if e.stderr:
                error_msg += f"\nError output: {e.stderr.decode('utf-8', errors='ignore')}"
            raise ValueError(error_msg)
        except Exception as e:
            raise ValueError(f"TTS synthesis failed: {str(e)}")

    def _wav_bytes_to_numpy(self, wav_bytes: bytes) -> np.ndarray:
        """Convert WAV bytes to numpy array."""
        try:
            import io
            import wave
            
            # Create a BytesIO object from the WAV bytes
            wav_io = io.BytesIO(wav_bytes)
            
            # Open as WAV file
            with wave.open(wav_io, 'rb') as wav_file:
                # Get audio parameters
                frames = wav_file.getnframes()
                sample_width = wav_file.getsampwidth()
                channels = wav_file.getnchannels()
                
                # Read audio data
                audio_bytes = wav_file.readframes(frames)
                
                # Convert to numpy array based on sample width
                if sample_width == 1:
                    # 8-bit audio
                    audio_array = np.frombuffer(audio_bytes, dtype=np.uint8)
                    audio_array = (audio_array.astype(np.float32) - 128) / 128.0
                elif sample_width == 2:
                    # 16-bit audio
                    audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
                    audio_array = audio_array.astype(np.float32) / 32768.0
                elif sample_width == 4:
                    # 32-bit audio
                    audio_array = np.frombuffer(audio_bytes, dtype=np.int32)
                    audio_array = audio_array.astype(np.float32) / 2147483648.0
                else:
                    raise ValueError(f"Unsupported sample width: {sample_width}")
                
                # Reshape for multi-channel audio
                if channels > 1:
                    audio_array = audio_array.reshape(-1, channels)
                    # Convert to mono by averaging channels
                    audio_array = np.mean(audio_array, axis=1)
                
                return audio_array
                
        except Exception as e:
            # Fallback: try using soundfile if available
            try:
                import soundfile as sf
                import io
                
                audio_array, _ = sf.read(io.BytesIO(wav_bytes))
                return audio_array.astype(np.float32)
            except ImportError:
                raise ValueError(f"Failed to decode WAV audio: {e}. Please install soundfile: pip install soundfile")
            except Exception as e2:
                raise ValueError(f"Failed to decode WAV audio: {e2}")


NODE_CLASS_MAPPINGS = {
    "DJZSpeak_v1": DJZSpeak_v1
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DJZSpeak_v1": "DJZ-Speak TTS v1"
}
